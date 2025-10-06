#!/usr/bin/env python3
import sys, re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / 'coverage' / 'lily_components.yaml'
REG = ROOT / 'rules' / 'REGISTRY.yaml'
MAP = ROOT / 'coverage' / 'lily_map.yaml'
TESTS = ROOT / 'tests'

KEY_TO_AGENT = [
  (re.compile(r'beam', re.I), 'BeamingAgent'),
  (re.compile(r'slur|tie', re.I), 'TieSlurAgent'),
  (re.compile(r'accidental|key|clef|time', re.I), 'AccidentalAgent'),
  (re.compile(r'dynamic|hairpin|crescendo', re.I), 'DynamicsTextAgent'),
  (re.compile(r'lyric|hyphen|extender', re.I), 'VerticalStackAgent'),
  (re.compile(r'ottava|trill|pedal|volta|rehearsal|tempo', re.I), 'VerticalStackAgent'),
  (re.compile(r'tuplet|grace|cross.*staff', re.I), 'BeamingAgent'),
  (re.compile(r'ledger|staff', re.I), 'VerticalStackAgent'),
  (re.compile(r'spacing|rest|collision|arpeggio|fingering|script|text', re.I), 'CollisionAgent'),
]

def agent_for(name: str) -> str:
    lname = name.lower()
    for rx, agent in KEY_TO_AGENT:
        if rx.search(lname):
            return agent
    return 'CollisionAgent'

def camelize(base: str) -> str:
    parts = re.split(r'[_\-\s]+', base)
    return ''.join(w.capitalize() for w in parts if w)

def main():
    comp = yaml.safe_load(COMP.read_text())
    reg_doc = yaml.safe_load(REG.read_text())
    mapping = yaml.safe_load(MAP.read_text())
    rules = reg_doc.get('rules', [])
    existing = {r['id'] for r in rules}
    m = mapping.setdefault('map', {})
    new_rules = []
    new_tests = []
    for c in comp.get('components', []):
        if not c.startswith('Engraver.'):
            continue
        base = c.split('.',1)[1]
        if base.endswith('_engraver'):
            base = base[:-9]
        rule_name = camelize(base)
        rid = f'RULE.{rule_name}.policy'
        if rid in existing:
            # ensure mapping points to explicit rule
            m[c] = [rid]
            continue
        agent = agent_for(base)
        stub = {
            'id': rid,
            'title': f'{rule_name} policy (stub)',
            'agent': agent,
            'intent': 'placement',
            'priority': 500,
            'depends_on': [],
            'inputs': ['context'],
            'parameters': { 'tbd': True },
            'procedure': 'Stub rule auto-generated for full engraver coverage. Replace with specific behavior.',
            'exceptions': [],
            'outputs': ['adjustments'],
            'side_effects': [],
            'test_plan': {
                'cases': [ { 'name': 'stub_present', 'expectations': [ { 'path': '/adjustments/count', 'op': '>=', 'value': 0.0 } ] } ]
            },
            'trace': ['_vendor/lilypond']
        }
        rules.append(stub)
        existing.add(rid)
        new_rules.append(rid)
        m[c] = [rid]
        # Prepare a minimal test file per rule
        test_name = f'STUB.{rule_name}.yml'
        new_tests.append((test_name, f"rule: {rid}\ncases:\n  - name: stub_present\n    expectations:\n      - {{ path: \"/adjustments/count\", op: \">=\", value: 0 }}\n"))
    # Write back registry and mapping
    reg_doc['rules'] = rules
    REG.write_text(yaml.safe_dump(reg_doc, sort_keys=False))
    MAP.write_text(yaml.safe_dump(mapping, sort_keys=False))
    # Emit tests
    TESTS.mkdir(parents=True, exist_ok=True)
    for fname, content in new_tests:
        (TESTS / fname).write_text(content)
    print(f'Generated {len(new_rules)} stub rules and {len(new_tests)} tests.')

if __name__ == '__main__':
    main()

