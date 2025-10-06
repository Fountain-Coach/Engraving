#!/usr/bin/env python3
# scripts/check_coverage.py — enforce Full Rule Set gates against manifest + OpenAPI.
import sys, os, json, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "rules" / "REGISTRY.yaml"
COV = ROOT / "coverage" / "manifest.json"
OAS = ROOT / "openapi" / "rules-as-functions.yaml"

def die(msg):
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(1)

def main():
    rules_doc = yaml.safe_load(REG.read_text())
    rules = [r["id"] for r in rules_doc.get("rules",[])]
    cov = json.loads(COV.read_text())
    oas = yaml.safe_load(OAS.read_text())
    ops = [oas["paths"][p]["post"]["operationId"] for p in oas.get("paths",{})]

    # Gate A: all rules present in OpenAPI
    missing_ops = sorted(set(rules) - set(ops))
    if missing_ops:
        die(f"OpenAPI missing operations for rules: {missing_ops}")

    # Gate B: coverage manifest parity
    declared = []
    ops_by_agent = {}
    for agent, info in cov["agents"].items():
        declared += info.get("declaredRules", [])
        for op in info.get("openapiOperations", []):
            ops_by_agent.setdefault(agent, []).append(op)

    extra_in_cov = sorted(set(declared) - set(rules))
    if extra_in_cov:
        die(f"Coverage manifest declares rules not in registry: {extra_in_cov}")

    # Gate C: each rule must have at least one test case (light check by name in /tests)
    tests_dir = ROOT / "tests"
    test_files = [p.read_text() for p in tests_dir.glob("*.yml")]
    tested = set()
    for txt in test_files:
        for r in rules:
            if f"rule: {r}" in txt:
                tested.add(r)
    missing_tests = sorted(set(rules) - tested)
    if missing_tests:
        die(f"Missing tests for rules: {missing_tests}")

    print("Coverage OK — all gates passed.")
if __name__ == "__main__":
    main()
