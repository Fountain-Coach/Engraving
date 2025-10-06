#!/usr/bin/env python3
import sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'coverage' / 'lily_components.yaml'

def find_engravers(lily: Path):
    engravers = set()
    for p in lily.rglob('lily/*.cc'):
        try:
            txt = p.read_text(errors='ignore')
        except Exception:
            continue
        for m in re.finditer(r'class\s+([A-Za-z0-9_]+)\s*:\s*public\s+Engraver', txt):
            engravers.add(m.group(1))
    return sorted(engravers)

def find_grobs(lily: Path):
    grobs = set()
    for p in list(lily.rglob('scm/*.scm')) + list(lily.rglob('*.cc')):
        try:
            txt = p.read_text(errors='ignore')
        except Exception:
            continue
        for m in re.finditer(r'\b([A-Z][A-Za-z0-9]+)\b', txt):
            name = m.group(1)
            if name in {'Grob','Engraver','Translator','Context','Paper','Font','String'}:
                continue
            if name.endswith('Grob') or name in {
                'NoteHead','Rest','Accidental','Beam','Slur','Tie','DynamicText','LyricText','OttavaBracket','VoltaBracket','StaffSymbol','Stem','Flag','TupletBracket','Fingering','RepeatTie','Breath','Clef','TimeSignature','KeySignature','LedgerLine','Hairpin','Script','Arpeggio','TrillSpanner','Crescendo','Decrescendo','Pedal','TextScript'}:
                grobs.add(name)
    return sorted(grobs)

def main():
    if len(sys.argv) < 2:
        print('Usage: generate_lily_components.py /path/to/lilypond', file=sys.stderr)
        sys.exit(2)
    lily = Path(sys.argv[1])
    if not lily.exists():
        print(f'Not found: {lily}', file=sys.stderr)
        sys.exit(2)
    engravers = find_engravers(lily)
    grobs = find_grobs(lily)
    lines = ["components:"]
    for e in engravers:
        lines.append(f"  - Engraver.{e}")
    for g in grobs:
        lines.append(f"  - Grob.{g}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f'Wrote {OUT} with {len(engravers)} engravers and {len(grobs)} grobs.')

if __name__ == '__main__':
    main()

