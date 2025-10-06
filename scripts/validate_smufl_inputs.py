#!/usr/bin/env python3
# scripts/validate_smufl_inputs.py — validate smufl_inputs in REGISTRY against whitelist.
import json, yaml, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
WL = json.loads((ROOT / "smufl" / "whitelist.json").read_text())
REG = yaml.safe_load((ROOT / "rules" / "REGISTRY.yaml").read_text())

allowed_glyphs = set(WL["glyphs"])
allowed_fields = set(WL["fields"])

errors = []
for r in REG.get("rules", []):
    for entry in r.get("smufl_inputs", []):
        if "." in entry:
            glyph, field = entry.split(".", 1)
        else:
            glyph, field = entry, None
        if glyph not in allowed_glyphs:
            errors.append(f"{r['id']}: unknown glyph '{glyph}'")
        if field and field not in allowed_fields:
            errors.append(f"{r['id']}: unknown field '{field}'")
if errors:
    print("SMuFL mapping errors:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("SMuFL mappings OK")
