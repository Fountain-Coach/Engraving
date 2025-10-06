# AGENTS.md — Source of Truth (Spec‑First)

This repo is language‑agnostic. Its final artifact is **OpenAPI 3.1 (rules‑as‑functions)** declaring **every** LilyPond‑grade engraving rule.

## 0) Principles
- Rules are **transparent, testable contracts**: typed inputs → decisions/outputs.
- **Traceability** to LilyPond docs/code is mandatory for every rule.
- **Determinism**: thresholds/penalties are named parameters; tests define measurable assertions.

## 1) FULL RULE SET CHARTER (Non‑Negotiable)
**Goal:** 100% of engraving behavior is represented as rules.
**Done when:**
1. **Coverage:** Each Agent has all behaviors encoded as rules (no gaps).
2. **Trace:** Every rule has resolvable `trace` references (doc/code).
3. **Tests:** Each rule has ≥1 case with numeric assertions & tolerances.
4. **Parameters:** All constants are explicit and named.
5. **OpenAPI Parity:** `openapi/rules-as-functions.yaml` has **one op per rule** (1:1 with this doc / registry).

## 2) Agents
- SpacingAgent
- VerticalStackAgent
- BeamingAgent
- TieSlurAgent
- CollisionAgent
- AccidentalAgent
- LedgerAgent
- DynamicsTextAgent
- PaginationAgent
- OpticalSizingAgent
- FontMetricsAgent

## 3) Rule Fields
`id, title, agent, intent, priority, depends_on, inputs, parameters, procedure, exceptions, outputs, side_effects, test_plan, trace`

## 4) Workflow
1) Author rules in `rules/REGISTRY.yaml`.
2) Run `scripts/build_openapi.py` → generates OpenAPI and updates coverage.
3) Add tests in `tests/*.yml`.
4) Run `scripts/check_coverage.py` → CI gates for full rule set trajectory.

## 5) Acceptance Criteria (Repo Level)
- OpenAPI contains every rule (`operationId == rule id`).
- Coverage manifest passes: declaredRules == openapiOperations; tests present; trace present.

## 6) Roadmap to Exhaustiveness
Enumerate grobs/interfaces → lift explicit rules → mine heuristics → add tests → lock rule → add OpenAPI op.

## 7) SMuFL Mapping (Required for Every Rule)
Each rule MUST declare the SMuFL metadata it consumes via `smufl_inputs`:
- Use canonical glyph names (e.g., `accidentalSharp`, `noteheadBlack`) and fields (e.g., `.bbox`, `.advance`, `.anchors.stemUp`).
- Examples:
  - `accidentalSharp.bbox`, `accidentalFlat.bbox`
  - `noteheadBlack.advance`, `noteheadWhole.bbox`
  - `dynamicForte.baseline`, `gClef.anchor.staffOrigin`
- OpenAPI exports this as vendor extension `x-smufl` on each rule operation.

## 8) Comprehensiveness Charter (Acceptance Gate)
A release is **COMPREHENSIVE** when all of the following hold:

1. **Rule Coverage**
   - Every engraving decision present in the gold-standard engraver is captured as a rule.
   - No implicit heuristics remain undocumented.

2. **SMuFL Mapping**
   - Each rule declares `smufl_inputs` referencing canonical glyph names and fields.
   - All entries pass `scripts/validate_smufl_inputs.py` (whitelist/schema).

3. **Typed Contracts**
   - Each rule appears in `openapi/rules-as-functions.typed.yaml` with precise input/output schemas.
   - No loss of information to untyped blobs; no `any` types for seeded agents.

4. **Traceability**
   - Each rule’s `trace` cites a primary source (LilyPond docs/code or an engraving text).
   - CI verifies link/anchor presence (policy: at least one resolvable anchor per rule).

5. **Tests and Metrics**
   - Each rule includes ≥1 machine-checkable test case with numeric assertions and tolerances.
   - Golden artifacts or IR fixtures are referenced where practical.

6. **CI Gates Passed**
   - `build_openapi.py` re-generates specs without diffs.
   - `check_coverage.py` confirms 1:1 parity between REGISTRY and OpenAPI; tests exist for each rule.
   - `validate_smufl_inputs.py` passes for all rules.

> When all six pillars are satisfied for the full set of rules, the repo is **done** (spec-complete).
