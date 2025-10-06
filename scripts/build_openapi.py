#!/usr/bin/env python3
# scripts/build_openapi.py — compile rules/REGISTRY.yaml into openapi/rules-as-functions.yaml and update coverage manifest.
import sys, os, json, yaml, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "rules" / "REGISTRY.yaml"
OUT = ROOT / "openapi" / "rules-as-functions.yaml"
COV = ROOT / "coverage" / "manifest.json"

def main():
    rules_doc = yaml.safe_load(REG.read_text())
    rules = rules_doc.get("rules", [])
    openapi = {
        "openapi": "3.1.0",
        "info": {
            "title": "Engraving Rules (Functions)",
            "version": "0.1.0",
            "description": "Generated from rules/REGISTRY.yaml on %s" % datetime.datetime.utcnow().isoformat()
        },
        "servers": [],
        "paths": {}
    }
    ops = []
    for r in rules:
        rid = r["id"]
        agent = r["agent"]
        # Use full rule id sans leading namespace to avoid path collisions
        slug = rid.split(".",1)[1].replace(".","-")
        path = f"/apply/{agent.replace('Agent','').lower()}/{slug}"
        # generic input/output schemas; implementors can refine further per rule
        req_schema = {"type":"object","additionalProperties":True}
        res_schema = {"type":"object","additionalProperties":True}
        openapi["paths"][path] = {
            "post": {
                "operationId": rid,
                "summary": r.get("title",""),
                "requestBody": {"required": True, "content": {"application/json":{"schema": req_schema}}},
                "responses": {"200":{"description":"OK","content":{"application/json":{"schema": res_schema}}}},
                "x-rule": {
                    k: r[k] for k in ["agent","intent","priority","depends_on","parameters","exceptions","trace","test_plan"] if k in r
                }
            }
        }
        ops.append(rid)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(yaml.safe_dump(openapi, sort_keys=False))
    # update coverage manifest openapiOperations
    cov = json.loads(COV.read_text())
    by_agent = {}
    for rid in ops:
        agent = rid.split(".")[1]
        by_agent.setdefault(agent, []).append(rid)
    for agent, info in cov["agents"].items():
        key = agent
        cov["agents"][agent]["openapiOperations"] = by_agent.get(agent, [])
    COV.write_text(json.dumps(cov, indent=2))
    print(f"Generated {OUT} with {len(ops)} operations. Updated coverage manifest.")

if __name__ == "__main__":
    main()
