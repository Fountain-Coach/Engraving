#!/usr/bin/env python3
import sys, re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / 'rules' / 'REGISTRY.yaml'
PROP = ROOT / 'coverage' / 'grob_properties.yaml'
PMAP = ROOT / 'coverage' / 'grob_property_map.yaml'
PREG = ROOT / 'coverage' / 'grob_property_registry.yaml'

def main():
    reg = yaml.safe_load(REG.read_text())
    props_doc = yaml.safe_load(PROP.read_text()) or {}
    pmap = yaml.safe_load(PMAP.read_text())
    # Merge canonical properties (if present)
    props_reg = []
    if PREG.exists():
        reg_doc = yaml.safe_load(PREG.read_text()) or {}
        props_reg = [e.get('name') for e in reg_doc.get('properties', []) if e.get('name')]
    rules = {r['id'] for r in reg.get('rules', [])}
    mapping = pmap.get('map', {})
    regex_entries = []
    exact_entries = {}
    catch_all = None
    for k, v in mapping.items():
        if isinstance(k, str) and len(k) >= 2 and k.startswith('/') and k.endswith('/'):
            try:
                rx = re.compile(k[1:-1], re.I)
                if rx.pattern == '.*':
                    catch_all = (rx, v)
                else:
                    regex_entries.append((rx, v))
            except Exception:
                pass
        else:
            exact_entries[k] = v
    missing = []
    invalid = []
    prop_list = props_doc.get('properties') or []
    all_props = set(prop_list) | set(props_reg)
    must_specific = {
        'X_offset','Y_offset','stencil','style','control_points','beam_thickness','beam_segments',
        'baseline','left_bound_info','right_bound_info','line_break_system_details','alteration',
        'KeySignature','TimeSignature','Clef','color','direction',
        'X_extent','Y_extent','bar_extent','baseline_skip','axes','align_dir','transparent','breakable','padding','thickness','beam_width','beaming'
    }
    for prop in sorted(all_props):
        targets = exact_entries.get(prop)
        matched_specific = targets is not None
        if targets is None:
            for rx, tv in regex_entries:
                if rx.search(prop):
                    targets = tv
                    matched_specific = True
                    break
        if targets is None and catch_all is not None:
            targets = catch_all[1]
        if not targets:
            missing.append(prop)
            continue
        if (prop in must_specific) and not matched_specific:
            missing.append(prop)
            continue
        for rid in targets:
            if rid not in rules:
                invalid.append((prop, rid))
    if missing or invalid:
        print('PROPERTY PARITY FAILED')
        if missing:
            print('Unmapped properties:', len(missing))
            for p in missing[:50]:
                print(f'  - {p}')
            if len(missing) > 50:
                print(f'  ... and {len(missing)-50} more')
        if invalid:
            print('Invalid rule references:')
            for p, rid in invalid:
                print(f'  - {p} -> {rid}')
        sys.exit(1)
    print('Property parity OK — all grob properties map to declared rules.')

if __name__ == '__main__':
    main()
