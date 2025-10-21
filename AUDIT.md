# Engraving Audit (Rules, Parity, Coverage)

This summary complements the CI audit (JSON artifact and job summary).
It reflects the repository state at the commit when this file was last updated.

## Summary
- Rules total: 90
- Status counts: ratified:90
- OpenAPI ops — untyped:90 typed:90 missing typed ops:0
- Ratified rules with tests: 90 / 90
- Lily components — Engravers:99 Grobs:26
- Grob property coverage — specific:132 regex:208 default:0

## CI Sources
- Job summary includes the audit JSON snippet
- Full audit JSON is uploaded as `engraving-audit` artifact in Engraving CI and Monorepo CI

## JSON Snapshot (for convenience)
```json
{
  "rules_total": 90,
  "status_counts": {
    "ratified": 90
  },
  "agent_counts": {
    "SpacingAgent": 6,
    "BeamingAgent": 10,
    "CollisionAgent": 21,
    "DynamicsTextAgent": 3,
    "VerticalStackAgent": 35,
    "TieSlurAgent": 2,
    "AccidentalAgent": 7,
    "PaginationAgent": 4,
    "LedgerAgent": 1,
    "OpticalSizingAgent": 1
  },
  "openapi_untyped_ops": 90,
  "openapi_typed_ops": 90,
  "missing_typed_ops": [],
  "rules_with_tests": 90,
  "engravings_total": 99,
  "grobs_total": 26,
  "unmapped_engravings": [],
  "property_coverage": {
    "specific": 132,
    "regex": 208,
    "default": 0
  }
}

```
