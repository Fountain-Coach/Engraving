#!/usr/bin/env python3
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / 'rules' / 'REGISTRY.yaml'

doc = yaml.safe_load(REG.read_text())
rules = doc.get('rules', [])
kept = []
removed = []
for r in rules:
    title = r.get('title','')
    if '(stub)' in title:
        removed.append(r['id'])
    else:
        kept.append(r)
doc['rules'] = kept
REG.write_text(yaml.safe_dump(doc, sort_keys=False))
print(f'Removed {len(removed)} stub rules')
