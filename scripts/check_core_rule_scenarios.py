#!/usr/bin/env python3
"""
Ensure core ratified rules have at least 2 scenarios across tests.
Core rules: spacing, beaming geometry/slope/subdivision, accidental lead-in,
tie/slur curvature, vertical stack, dynamics align, rest & beam collisions.
"""
import sys, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / 'rules' / 'REGISTRY.yaml'
TESTS = ROOT / 'tests'

CORE = {
  'RULE.Spacing.duration_base_with_optical_corrections',
  'RULE.NoteSpacing.spacing_policy',
  'RULE.Beaming.geometry_slope_and_segments',
  'RULE.Beaming.slope_with_clearance',
  'RULE.Beaming.subdivision_preference',
  'RULE.Accidental.leading_padding_and_column_inflation',
  'RULE.Tie.curvature_selection_with_clearance',
  'RULE.Slur.curvature_choice_with_collision_penalty',
  'RULE.Vertical.min_dist_padding_and_stretch',
  'RULE.Dynamics.align_with_noteheads_and_stems',
  'RULE.RestCollision.resolve_overlaps',
  'RULE.BeamCollision.resolve_overlaps',
}

def main():
    reg = yaml.safe_load(REG.read_text())
    ratified = {r['id'] for r in reg.get('rules', []) if r.get('status') == 'ratified'}
    counts = {}
    for tf in TESTS.glob('*.yml'):
        try:
            doc = yaml.safe_load(tf.read_text()) or {}
        except Exception:
            continue
        rid = doc.get('rule')
        if not isinstance(rid, str):
            continue
        n = len(doc.get('cases') or [])
        counts[rid] = counts.get(rid, 0) + n
    missing = []
    for rid in sorted(CORE):
        if rid in ratified and counts.get(rid, 0) < 2:
            missing.append((rid, counts.get(rid, 0)))
    if missing:
        print('CORE RULE COVERAGE FAILED: fewer than 2 scenarios')
        for rid, c in missing:
            print(f' - {rid}: {c} cases')
        sys.exit(1)
    print('Core rule coverage OK — all core ratified rules have >= 2 scenarios.')

if __name__ == '__main__':
    main()

