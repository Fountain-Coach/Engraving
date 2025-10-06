# Engraving — Spec‑First Starter (Complete Bundle)

This is a **complete, language‑agnostic starter** to capture the **FULL RULE SET** of LilyPond‑grade engraving rules,
and express each rule as an **OpenAPI 3.1 function contract**.

## What’s included
- `AGENTS.md`: source of truth + Full Rule Set Charter
- `rules/REGISTRY.yaml`: author rules once
- `scripts/build_openapi.py`: compiles OpenAPI from the registry + updates coverage
- `scripts/check_coverage.py`: verifies gates (OpenAPI parity + tests present)
- `openapi/rules-as-functions.yaml`: generated spec (seed included; regenerate after edits)
- `schemas/rule.schema.json`: JSON Schema for rule objects/tests
- `tests/*.yml`: language‑agnostic rule tests
- `coverage/manifest.json`: CI coverage manifest
- `requirements.txt`: Python deps (PyYAML)

## Quick start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/build_openapi.py
python scripts/check_coverage.py
python scripts/validate_smufl_inputs.py
python scripts/check_parity.py
```

> Regenerated on 2025-10-06T04:37:59.386060 UTC.

## Swift 6 Code Generation (First-Class)
A **typed** OpenAPI is provided at `openapi/rules-as-functions.typed.yaml` for high‑quality codegen.

### Use Apple’s Swift OpenAPI Generator
```bash
cd codegen/swift/RulesKit-SPM
swift build
```
This invokes the generator plugin, producing Swift types and operation handlers for each rule.

### Validate SMuFL mappings
```bash
python scripts/validate_smufl_inputs.py
```

### CI gates
```bash
python scripts/build_openapi.py      # refresh untyped spec + coverage
python scripts/check_coverage.py     # parity + tests present
python scripts/validate_smufl_inputs.py  # SMuFL mapping whitelist
python scripts/check_parity.py       # ALL rules mapped (Lily components → rules)
```
