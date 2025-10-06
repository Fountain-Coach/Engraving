# Engraving — Rules as Functions (Spec‑First, Ratified)

[![Engraving CI](https://github.com/Fountain-Coach/Engraving/actions/workflows/ci.yml/badge.svg)](https://github.com/Fountain-Coach/Engraving/actions/workflows/ci.yml)
[![RulesKit Swift Build](https://github.com/Fountain-Coach/Engraving/actions/workflows/ruleskit.yml/badge.svg)](https://github.com/Fountain-Coach/Engraving/actions/workflows/ruleskit.yml)

Spec‑first definition of LilyPond‑grade engraving as OpenAPI 3.1 “rules as functions”, with a typed spec for high‑quality codegen and CI gates for determinism.

Highlights
- Single source of truth: `rules/REGISTRY.yaml` (81 rules, all ratified)
- Deterministic OpenAPI: untyped + typed in lockstep, zero placeholders
- Ratified schema lock enforced in CI (no silent breaking changes)
- Full LilyPond component + grob property parity gates
- Swift 6 codegen target (`RulesKit`) built in CI via `swift-openapi-generator`

---

## Repository Layout
- `AGENTS.md` — contributor guide and conventions
- `rules/REGISTRY.yaml` — author rules once (title, inputs/outputs, parameters, trace, test_plan, smufl_inputs, status)
- `openapi/` — generated specs
  - `rules-as-functions.yaml` (untyped)
  - `rules-as-functions.typed.yaml` (typed)
  - `typed-ratified-lock.json` (CI‑enforced digests of ratified request/response schemas)
- `scripts/` — tooling and gates
  - Builders: `build_openapi.py`, `build_openapi_typed.py`
  - Gates: `check_parity.py`, `check_property_parity.py`, `lint_typed_openapi.py`, `validate_smufl_inputs.py`, `check_rule_tests.py`, `check_core_rule_scenarios.py`
  - Lock: `update_ratified_lock.py`
- `coverage/` — coverage manifests and LilyPond component/property maps
- `smufl/` — SMuFL glyph whitelist and fields used by rules
- `tests/` — language‑agnostic YAML tests per rule
- `codegen/swift/RulesKit-SPM/` — Swift 6 package that builds against the typed spec

## Quick Start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate specs and run all gates
python scripts/build_openapi.py
python scripts/build_openapi_typed.py
python scripts/validate_smufl_inputs.py
python scripts/check_parity.py
python scripts/check_property_parity.py
python scripts/lint_typed_openapi.py
python scripts/check_rule_tests.py
python scripts/check_core_rule_scenarios.py
```

## Editing Rules
1) Add or update a rule in `rules/REGISTRY.yaml`.
   - Provide: `title`, `inputs`, `outputs`, `parameters`, `trace`, `test_plan.cases`, and `smufl_inputs` (for glyph‑dependent rules).
   - Set an appropriate `status`: `draft` → `provisional` → `ratified`.
2) Regenerate specs:
   - `python scripts/build_openapi.py && python scripts/build_openapi_typed.py`
3) Add or update tests in `tests/*.yml`.
4) Run gates (see Quick Start). When marking a rule `ratified` or changing a ratified schema:
   - Update the lock: `python scripts/update_ratified_lock.py`
   - Commit the updated `openapi/typed-ratified-lock.json`.

## Determinism & Gates
- Typed/untyped path parity; arrays must have `minItems`.
- No placeholders (no `RuleInput`/`RuleOutput`, no `StrictEmpty`).
- Vendor extensions: every path has `x-rule` and non‑empty `trace`; glyph‑dependent families have `x-smufl` or `x-rule.smufl_inputs`.
- Ratified schema lock: typed request/response digests must match `typed-ratified-lock.json`.
- LilyPond parity: all `Grob.*` and `Engraver.*` mapped in coverage; `scripts/check_parity.py` passes.
- Grob property parity: `coverage/grob_property_map.yaml` covers the canonical registry and must‑specific classes; `scripts/check_property_parity.py` passes.
- Tests: every ratified rule has ≥1 test; core families have ≥2 scenarios (CI‑enforced).

## SMuFL Glyphs
- Whitelist is defined in `smufl/whitelist.json`.
- Validate declared glyph inputs with: `python scripts/validate_smufl_inputs.py`.

## Swift 6 Code Generation (RulesKit)
```bash
cd codegen/swift/RulesKit-SPM
swift build -c release
```
- Uses the `swift-openapi-generator` plugin targeting `Sources/RulesKit/openapi/rules-as-functions.yaml` (typed spec is copied in CI).
- The GitHub Actions workflow `RulesKit Swift Build` builds on macOS.

## CI Workflows
- Engraving CI: spec builders, parity/property/SMuFL gates, typed linter, test coverage gates.
- RulesKit Swift Build: macOS job that codegens + builds the Swift package.

## Definition of Done
- All rules present and marked `ratified` with tests.
- All gates green (typed linter + lock, parity/property/SMuFL, tests, core coverage).
- Codegen target builds without manual edits.

## Contributing
- Follow `AGENTS.md` for conventions and commit style.
- For ratified rules, include migration notes in PR descriptions when changing schemas and refresh the lock.
- Add tests alongside rule changes; for core families, provide at least two scenarios.

## License
See the repository’s license. Third‑party tools remain under their respective licenses.
