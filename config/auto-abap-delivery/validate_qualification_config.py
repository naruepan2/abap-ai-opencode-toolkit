#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
try:
    import yaml
except ImportError:  # Python 3.15 has no PyYAML wheel; ruamel.yaml is pure Python
    from ruamel.yaml import YAML
    class _YamlCompat:
        @staticmethod
        def safe_load(text):
            return YAML(typ="safe").load(text)
    yaml = _YamlCompat()
from jsonschema import Draft202012Validator, FormatChecker

p = argparse.ArgumentParser(description="Validate Qualification YAML against its JSON Schema")
p.add_argument("config", help="Path to qualification YAML")
p.add_argument("schema", help="Path to JSON Schema")
a = p.parse_args()

try:
    data = yaml.safe_load(Path(a.config).read_text(encoding="utf-8"))
    schema = json.loads(Path(a.schema).read_text(encoding="utf-8"))
except Exception as exc:
    print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
    sys.exit(1)

validator = Draft202012Validator(schema, format_checker=FormatChecker())
errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
result = {
    "valid": not errors,
    "errors": [
        {
            "path": "/" + "/".join(str(x) for x in err.absolute_path),
            "message": err.message
        }
        for err in errors
    ]
}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if result["valid"] else 1)
