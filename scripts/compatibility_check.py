#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
try:
    import yaml
except ImportError:  # Python 3.15 has no PyYAML wheel; ruamel.yaml is pure Python
    from ruamel.yaml import YAML
    class _YamlCompat:
        @staticmethod
        def safe_load(text):
            return YAML(typ="safe").load(text)
    yaml = _YamlCompat()
root=Path(__file__).resolve().parents[1]
errors=[]
for p in [root/'config/auto-abap-delivery/qualification-config.example.yaml', root/'config/auto-abap-delivery/qualification-config.schema.json']:
    if not p.exists(): errors.append(f'missing {p.relative_to(root)}')
try:
    cfg=yaml.safe_load((root/'config/auto-abap-delivery/qualification-config.example.yaml').read_text())
    json.loads((root/'config/auto-abap-delivery/qualification-config.schema.json').read_text())
    if cfg['default_policy']['unqualified_scope']['execution_mode']!='attended': errors.append('unqualified default must be attended')
    if cfg['default_policy']['qualified_scope']['execution_mode']!='unattended': errors.append('qualified default must be unattended')
except Exception as e: errors.append(str(e))
print(json.dumps({'valid':not errors,'errors':errors},indent=2));sys.exit(1 if errors else 0)
