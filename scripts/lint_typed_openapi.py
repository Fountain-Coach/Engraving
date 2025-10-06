#!/usr/bin/env python3
"""
Lint the typed OpenAPI for determinism and concreteness:
- For every array schema, require `minItems`.
- For every path in untyped spec, require an equivalent path in typed spec.
- For typed request/response, forbid GenericInput/GenericOutput.
"""
import sys, yaml, json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNTYPED = ROOT / 'openapi' / 'rules-as-functions.yaml'
TYPED = ROOT / 'openapi' / 'rules-as-functions.typed.yaml'
LOCK = ROOT / 'openapi' / 'typed-ratified-lock.json'

def _resolve_ref(schema, comps):
    if isinstance(schema, dict) and '$ref' in schema:
        ref = schema['$ref']
        if not ref.startswith('#/components/schemas/'):
            return schema
        name = ref.split('/')[-1]
        target = comps.get(name)
        if target is None:
            return schema
        return _resolve_ref(target, comps)
    if isinstance(schema, dict):
        return {k: _resolve_ref(v, comps) for k, v in schema.items()}
    if isinstance(schema, list):
        return [_resolve_ref(v, comps) for v in schema]
    return schema

def _digest(obj):
    try:
        data = json.dumps(obj, sort_keys=True, separators=(',',':'))
    except Exception:
        data = str(obj)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def scan_arrays(name, node, errs, path='$'):
    if isinstance(node, dict):
        t = node.get('type')
        if t == 'array':
            if 'minItems' not in node:
                errs.append(f"Array at {path} missing minItems")
        for k,v in node.items():
            scan_arrays(name, v, errs, path+f".{k}")
    elif isinstance(node, list):
        for i,v in enumerate(node):
            scan_arrays(name, v, errs, path+f"[{i}]")

def main():
    unt = yaml.safe_load(UNTYPED.read_text())
    typ = yaml.safe_load(TYPED.read_text())
    u_paths = set(unt.get('paths', {}).keys())
    t_paths = set(typ.get('paths', {}).keys())
    missing = sorted(u_paths - t_paths)
    errs = []
    if missing:
        errs.append(f"Typed spec missing {len(missing)} paths found in untyped: e.g. {missing[:5]}")
    extra = sorted(t_paths - u_paths)
    if extra:
        errs.append(f"Typed spec has {len(extra)} extra paths not in untyped (stale): e.g. {extra[:5]}")

    # Check arrays in components
    comps = typ.get('components', {}).get('schemas', {})
    for name, schema in comps.items():
        scan_arrays(name, schema, errs, path=f'#/components/schemas/{name}')

    # Check for Generic fallbacks anywhere
    s = TYPED.read_text()
    if 'GenericInput' in s or 'GenericOutput' in s:
        errs.append('GenericInput/GenericOutput present in typed spec')

    # Check each typed path has x-rule with trace and (when applicable) x-smufl
    for p, op in typ.get('paths', {}).items():
        post = op.get('post', {})
        xr = post.get('x-rule')
        if not xr:
            errs.append(f"Path {p} missing x-rule vendor extension")
            continue
        # Require status in x-rule
        status = xr.get('status')
        if status not in ('draft','provisional','ratified'):
            errs.append(f"Path {p} x-rule.status missing or invalid (expected draft|provisional|ratified)")
        tr = xr.get('trace', [])
        if not tr:
            errs.append(f"Path {p} x-rule.trace is empty")
        # x-smufl may be present in typed or via x-rule.smufl_inputs in untyped
        # We accept absence for non-glyph rules (Pagination, Vertical), but require for Accidental/Beaming/Spacing families
        fam = p.split('/')[2] if p.startswith('/apply/') else ''
        needs_smufl = fam.lower() in ('accidental','beaming','spacing','ledger','slur','tieslur','notespace','dynamicstext')
        if needs_smufl and not (post.get('x-smufl') or (xr.get('smufl_inputs'))):
            errs.append(f"Path {p} missing x-smufl or x-rule.smufl_inputs for glyph-dependent family")

    # Ratified schema lock enforcement
    comps = typ.get('components', {}).get('schemas', {})
    ratified = {}
    for p, op in typ.get('paths', {}).items():
        post = op.get('post', {})
        xr = post.get('x-rule') or {}
        if xr.get('status') == 'ratified':
            rid = post.get('operationId')
            req = post.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema')
            res = post.get('responses', {}).get('200', {}).get('content', {}).get('application/json', {}).get('schema')
            req_resolved = _resolve_ref(req, comps) if req else None
            res_resolved = _resolve_ref(res, comps) if res else None
            ratified[rid] = {
                'path': p,
                'request': _digest(req_resolved) if req_resolved is not None else None,
                'response': _digest(res_resolved) if res_resolved is not None else None,
            }
    if LOCK.exists():
        try:
            locked = json.loads(LOCK.read_text())
        except Exception:
            errs.append('Ratified lock exists but is unreadable JSON')
            locked = {}
        for rid, cur in ratified.items():
            prev = locked.get(rid)
            if not prev:
                errs.append(f"Ratified lock missing entry for {rid}; run update_ratified_lock.py with a migration note")
                continue
            if prev.get('request') != cur.get('request') or prev.get('response') != cur.get('response'):
                errs.append(f"Ratified schema changed for {rid} at {cur['path']} — add migration note in x-rule and run update_ratified_lock.py")
    else:
        errs.append('Ratified lock file missing: openapi/typed-ratified-lock.json — generate via scripts/update_ratified_lock.py')

    if errs:
        print('TYPED OPENAPI LINT FAILED')
        for e in errs:
            print(' -', e)
        sys.exit(1)
    print('Typed OpenAPI lint passed')

if __name__ == '__main__':
    main()
