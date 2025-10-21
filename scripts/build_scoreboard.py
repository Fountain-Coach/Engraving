#!/usr/bin/env python3
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(p):
    return yaml.safe_load(p.read_text())

def main():
    reg = load_yaml(ROOT / 'rules' / 'REGISTRY.yaml')
    lmap = load_yaml(ROOT / 'coverage' / 'lily_map.yaml')
    rules = {r['id']: r for r in reg.get('rules', [])}

    eng_map = lmap.get('map', {})
    engs = {k: v for k, v in eng_map.items() if str(k).startswith('Engraver.')}

    done = []
    partial = []
    todo = []
    details = {}
    for eng, rids in engs.items():
        rids = list(rids or [])
        unknown = [rid for rid in rids if rid not in rules]
        statuses = [rules[rid]['status'] for rid in rids if rid in rules]
        if not rids or unknown:
            todo.append(eng)
            details[eng] = {'rules': rids, 'unknown': unknown, 'statuses': statuses}
        elif all(s == 'ratified' for s in statuses):
            done.append(eng)
            details[eng] = {'rules': rids, 'unknown': unknown, 'statuses': statuses}
        else:
            partial.append(eng)
            details[eng] = {'rules': rids, 'unknown': unknown, 'statuses': statuses}

    lines = []
    lines.append('# Engraver Parity Scoreboard')
    lines.append('')
    lines.append('This scoreboard classifies each Engraver.* family by the status of the rules it maps to:')
    lines.append('- Done: all mapped rules exist and are ratified')
    lines.append('- Partial: mapped rules exist but some are draft/provisional')
    lines.append('- Todo: missing mapping or rules unknown to the registry')
    lines.append('')
    lines.append('## Summary')
    lines.append(f'- Total Engraver families: {len(engs)}')
    lines.append(f'- Done: {len(done)}')
    lines.append(f'- Partial: {len(partial)}')
    lines.append(f'- Todo: {len(todo)}')
    lines.append('')
    def section(title, items):
        lines.append(f'## {title}')
        if not items:
            lines.append('- (none)')
        else:
            for eng in sorted(items):
                info = details.get(eng, {})
                rules_list = ', '.join(info.get('rules', []))
                statuses_list = ', '.join(info.get('statuses', []))
                unknown_list = ', '.join(info.get('unknown', []))
                lines.append(f'- {eng}:')
                lines.append(f'  - rules: {rules_list}')
                if unknown_list:
                    lines.append(f'  - unknown: {unknown_list}')
                lines.append(f'  - statuses: {statuses_list}')
        lines.append('')

    section('Done', done)
    section('Partial', partial)
    section('Todo', todo)

    (ROOT / 'SCOREBOARD.md').write_text('\n'.join(lines))
    print('Wrote SCOREBOARD.md')

if __name__ == '__main__':
    main()

