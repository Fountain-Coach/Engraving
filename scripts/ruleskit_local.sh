#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
PKG="$ROOT/codegen/swift/RulesKit-SPM"

echo "[1/6] Build untyped/typed OpenAPI"
python3 "$ROOT/scripts/build_openapi.py"
python3 "$ROOT/scripts/build_openapi_typed.py"

echo "[2/6] Run spec gates (typed linter, property parity)"
python3 "$ROOT/scripts/lint_typed_openapi.py"
python3 "$ROOT/scripts/check_property_parity.py"

echo "[3/6] Sync typed spec into Swift package"
mkdir -p "$PKG/Sources/RulesKit/openapi"
cp "$ROOT/openapi/rules-as-functions.typed.yaml" "$PKG/Sources/RulesKit/openapi/rules-as-functions.yaml"
cp "$PKG/Sources/RulesKit/openapi/rules-as-functions.yaml" "$PKG/Sources/RulesKit/openapi.yaml"

echo "[4/6] Swift build (clean)"
pushd "$PKG" >/dev/null
swift package clean || true
set +e
OUT=$(swift build -c release 2>&1)
STATUS=$?
set -e
popd >/dev/null

if [[ $STATUS -ne 0 ]]; then
  echo "\n[!] Swift build failed. Summarizing common causes:" >&2
  echo "$OUT" >&2
  # Detect missing schema reference
  if grep -Eo "reference=#/components/schemas/[A-Za-z0-9_]+" <<< "$OUT" >/dev/null; then
    MISS=$(grep -Eo "reference=#/components/schemas/[A-Za-z0-9_]+" <<< "$OUT" | head -n1 | sed 's#reference=#/components/schemas/##')
    echo "\n>> Missing schema detected: $MISS" >&2
    echo ">> Add a put('$MISS', { ... }) definition to scripts/build_openapi_typed.py, then re-run:" >&2
    echo "   python3 scripts/build_openapi_typed.py && python3 scripts/update_ratified_lock.py" >&2
  fi
  exit $STATUS
fi

echo "[5/6] Swift build OK"
echo "[6/6] Done. RulesKit codegen validated locally."

