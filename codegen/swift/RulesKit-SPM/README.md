# RulesKit (Swift 6) — Codegen Adapter

This SPM package demonstrates **Swift 6** code generation from the spec‑first OpenAPI.

## How it works
- The `swift-openapi-generator` plugin reads `openapi/rules-as-functions.typed.yaml`.
- It generates Swift types & entrypoints for each **rule function**.
- You then map generated entrypoints to your engraving engine implementation.

## Commands
```bash
swift build
# If plugin is installed, generated sources appear under .build/plugins/.../Outputs
```

> Note: The plugin fetch requires network access. If you’re offline, vendor the generated sources after a first run.
