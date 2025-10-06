#!/usr/bin/env python3
"""
Lint the typed OpenAPI for determinism and concreteness:
- For every array schema, require `minItems`.
- For every path in untyped spec, require an equivalent path in typed spec.
- For typed request/response, forbid GenericInput/GenericOutput.
"""
import sys, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNTYPED = ROOT / 'openapi' / 'rules-as-functions.yaml'
TYPED = ROOT / 'openapi' / 'rules-as-functions.typed.yaml'

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

    if errs:
        print('TYPED OPENAPI LINT FAILED')
        for e in errs:
            print(' -', e)
        sys.exit(1)
    print('Typed OpenAPI lint passed')

if __name__ == '__main__':
    main()
