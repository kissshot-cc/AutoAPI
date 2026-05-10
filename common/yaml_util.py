from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_ROOT = Path(__file__).resolve().parent.parent


def load_yaml(filename: str) -> dict[str, Any]:
    path = _ROOT / "data" / filename
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
