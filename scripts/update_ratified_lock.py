#!/usr/bin/env python3
"""
Update the ratified schema lock from the current typed OpenAPI.
Writes openapi/typed-ratified-lock.json with request/response digests for all
rules where x-rule.status == 'ratified'.

If you are intentionally changing a ratified schema, include a migration note
in x-rule (e.g., x-rule.migration: { id: R###, note: ... }) in REGISTRY.yaml,
then re-run this script and commit the updated lock.
"""
import json, hashlib, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
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
    data = json.dumps(obj, sort_keys=True, separators=(',',':'))
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def main():
    doc = yaml.safe_load(TYPED.read_text())
    comps = doc.get('components', {}).get('schemas', {})
    out = {}
    for path, op in (doc.get('paths') or {}).items():
        post = op.get('post') or {}
        xr = post.get('x-rule') or {}
        if xr.get('status') != 'ratified':
            continue
        rid = post.get('operationId')
        req = post.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema')
        res = post.get('responses', {}).get('200', {}).get('content', {}).get('application/json', {}).get('schema')
        req_resolved = _resolve_ref(req, comps) if req else None
        res_resolved = _resolve_ref(res, comps) if res else None
        out[rid] = {
            'path': path,
            'request': _digest(req_resolved) if req_resolved is not None else None,
            'response': _digest(res_resolved) if res_resolved is not None else None,
        }
    LOCK.write_text(json.dumps(out, indent=2))
    print(f'Wrote ratified lock with {len(out)} entries to {LOCK}')

if __name__ == '__main__':
    main()

