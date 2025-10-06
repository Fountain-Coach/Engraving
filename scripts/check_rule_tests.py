#!/usr/bin/env python3
"""
Ensure every ratified rule in rules/REGISTRY.yaml has at least one YAML test in tests/.
Passes for non-ratified rules (draft/provisional).
"""
import sys, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / 'rules' / 'REGISTRY.yaml'
TESTS = ROOT / 'tests'

def main():
    reg = yaml.safe_load(REG.read_text())
    ratified = [r['id'] for r in reg.get('rules', []) if r.get('status') == 'ratified']
    covered = set()
    for tf in TESTS.glob('*.yml'):
        try:
            doc = yaml.safe_load(tf.read_text()) or {}
        except Exception:
            continue
        rid = doc.get('rule')
        if isinstance(rid, str):
            covered.add(rid)
    missing = [rid for rid in ratified if rid not in covered]
    if missing:
        print('RULE TESTS GATE FAILED: ratified rules without tests:')
        for rid in missing:
            print(' -', rid)
        sys.exit(1)
    print('Rule tests OK — all ratified rules have at least one test.')

if __name__ == '__main__':
    main()

