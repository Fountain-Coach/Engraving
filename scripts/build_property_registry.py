#!/usr/bin/env python3
import sys, re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'coverage' / 'grob_property_registry.yaml'

def build_registry(lily: Path):
    entries = []
    files = list(lily.rglob('scm/define-grob-properties.scm'))
    if not files:
        files = list(lily.rglob('**/define-grob-properties.scm'))
    for p in files:
        try:
            txt = p.read_text(errors='ignore')
        except Exception:
            continue
        # Pattern: (left-bound-info ,symbol-key-alist? "desc...")
        for m in re.finditer(r"\(\s*([A-Za-z0-9_-]+)\s*,\s*([A-Za-z0-9_-?]+)\s+\"([^\"]*)\"\s*\)\)", txt):
            name = m.group(1).replace('-', '_')
            typ = m.group(2)
            desc = m.group(3)
            entries.append({'name': name, 'type': typ, 'description': desc})
        # Also look for define-grob-property 'name type? "desc"
        for m in re.finditer(r"define-grob-property\s+'([A-Za-z0-9_-]+)'\s+([A-Za-z0-9_-?]+)\s+\"([^\"]*)\"", txt):
            name = m.group(1).replace('-', '_')
            typ = m.group(2)
            desc = m.group(3)
            entries.append({'name': name, 'type': typ, 'description': desc})
    # Deduplicate by name preferring first occurrence
    seen = set()
    uniq = []
    for e in entries:
        if e['name'] in seen:
            continue
        seen.add(e['name'])
        uniq.append(e)
    return uniq

def main():
    if len(sys.argv) < 2:
        print('Usage: build_property_registry.py /path/to/lilypond', file=sys.stderr)
        sys.exit(2)
    lily = Path(sys.argv[1])
    if not lily.exists():
        print(f'Not found: {lily}', file=sys.stderr)
        sys.exit(2)
    reg = build_registry(lily)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(yaml.safe_dump({'properties': reg}, sort_keys=False))
    print(f'Wrote {OUT} with {len(reg)} canonical properties.')

if __name__ == '__main__':
    main()

