from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

_ROOT = Path(__file__).resolve().parent.parent
_SCHEMAS_DIR = _ROOT / "config" / "schemas"
_cache: dict[str, dict] = {}


def _load_schema(name: str) -> dict:
    if name not in _cache:
        path = _SCHEMAS_DIR / f"{name}.json"
        if not path.exists():
            raise FileNotFoundError(f"Schema not found: {path}")
        with open(path, encoding="utf-8") as f:
            _cache[name] = json.load(f)
    return _cache[name]


def validate(response: dict[str, Any], schema_name: str) -> None:
    """校验响应是否符合指定 JSONSchema。"""
    schema = _load_schema(schema_name)
    try:
        jsonschema.validate(instance=response, schema=schema)
    except jsonschema.ValidationError as e:
        path = ".".join(str(p) for p in e.absolute_path) if e.absolute_path else "(root)"
        raise AssertionError(
            f"JSONSchema validation failed for '{schema_name}' at '{path}': {e.message}"
        ) from e
