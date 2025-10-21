#!/usr/bin/env python3
import re, sys, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(p):
    return yaml.safe_load(p.read_text())

def main():
    reg = load_yaml(ROOT / 'rules' / 'REGISTRY.yaml')
    ut = load_yaml(ROOT / 'openapi' / 'rules-as-functions.yaml')
    tt = load_yaml(ROOT / 'openapi' / 'rules-as-functions.typed.yaml')
    comps = load_yaml(ROOT / 'coverage' / 'lily_components.yaml')
    lmap = load_yaml(ROOT / 'coverage' / 'lily_map.yaml')
    preg = load_yaml(ROOT / 'coverage' / 'grob_property_registry.yaml')
    pmap = load_yaml(ROOT / 'coverage' / 'grob_property_map.yaml')

    rules = reg.get('rules', [])
    rule_ids = {r['id'] for r in rules}
    status = {}
    agents = {}
    for r in rules:
        status[r.get('status','unknown')] = status.get(r.get('status','unknown'),0)+1
        agents[r.get('agent','Unknown')] = agents.get(r.get('agent','Unknown'),0)+1

    ut_ops = {op['post']['operationId'] for _,op in (ut.get('paths') or {}).items()}
    tt_ops = {op['post']['operationId'] for _,op in (tt.get('paths') or {}).items()}

    # tests
    rule_to_tests = {rid:0 for rid in rule_ids}
    for tf in sorted((ROOT/'tests').glob('*.yml')):
        txt = tf.read_text(errors='ignore')
        m = re.search(r'^rule:\s*(\S+)', txt, re.M)
        if m and m.group(1) in rule_to_tests:
            # accumulate number of cases per file
            cases = re.findall(r'^\s*-\s*name:', txt, re.M)
            rule_to_tests[m.group(1)] += max(1, len(cases))
    tested = sum(1 for k,v in rule_to_tests.items() if v>0)

    engs = [c for c in comps.get('components',[]) if str(c).startswith('Engraver.')]
    grobs = [c for c in comps.get('components',[]) if str(c).startswith('Grob.')]
    mapped = set((lmap.get('map') or {}).keys())
    unmapped_engs = [e for e in engs if e not in mapped]

    props = [p['name'] for p in preg.get('properties',[])]
    mapping = pmap.get('map',{})
    regex_entries = []
    for k in mapping.keys():
        if isinstance(k,str) and len(k)>=2 and k.startswith('/') and k.endswith('/'):
            try:
                regex_entries.append((k,re.compile(k[1:-1], re.I)))
            except Exception:
                pass
    def classify(prop):
        if prop in mapping: return 'specific'
        for _,rx in regex_entries:
            if rx.search(prop):
                return 'regex'
        return 'default'
    classes = {'specific':0,'regex':0,'default':0}
    for p in props:
        classes[classify(p)] += 1

    report = {
        'rules_total': len(rules),
        'status_counts': status,
        'agent_counts': agents,
        'openapi_untyped_ops': len(ut_ops),
        'openapi_typed_ops': len(tt_ops),
        'missing_typed_ops': sorted(list(rule_ids-tt_ops)),
        'rules_with_tests': tested,
        'engravings_total': len(engs),
        'grobs_total': len(grobs),
        'unmapped_engravings': unmapped_engs,
        'property_coverage': classes,
    }
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()

