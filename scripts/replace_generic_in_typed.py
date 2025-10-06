#!/usr/bin/env python3
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPED = ROOT / 'openapi' / 'rules-as-functions.typed.yaml'

def replace_refs(node):
    if isinstance(node, dict):
        for k,v in list(node.items()):
            if k == '$ref' and isinstance(v, str) and v.endswith('/GenericInput'):
                node[k] = v.replace('/GenericInput','/StrictEmpty')
            if k == '$ref' and isinstance(v, str) and v.endswith('/GenericOutput'):
                node[k] = v.replace('/GenericOutput','/StrictEmpty')
            else:
                replace_refs(v)
    elif isinstance(node, list):
        for v in node:
            replace_refs(v)

doc = yaml.safe_load(TYPED.read_text())
replace_refs(doc)
schemas = doc.setdefault('components',{}).setdefault('schemas',{})
if 'GenericInput' in schemas:
    del schemas['GenericInput']
if 'GenericOutput' in schemas:
    del schemas['GenericOutput']
schemas.setdefault('StrictEmpty', { 'type':'object', 'additionalProperties': False })
TYPED.write_text(yaml.safe_dump(doc, sort_keys=False))
print('Replaced Generic* with StrictEmpty in typed spec')
