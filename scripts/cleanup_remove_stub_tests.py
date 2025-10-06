#!/usr/bin/env python3
import yaml, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = yaml.safe_load((ROOT/'rules'/'REGISTRY.yaml').read_text())
rules = {r['id'] for r in REG.get('rules', [])}
tests_dir = ROOT/'tests'
removed = []
for p in tests_dir.glob('*.yml'):
    try:
        txt = p.read_text()
    except Exception:
        continue
    m = re.match(r"\s*rule:\s*([A-Za-z0-9\._]+)", txt)
    if not m:
        continue
    rid = m.group(1).strip()
    if rid.endswith('.policy') and rid not in rules:
        p.unlink()
        removed.append(p.name)
print(f'Removed {len(removed)} stub tests')
