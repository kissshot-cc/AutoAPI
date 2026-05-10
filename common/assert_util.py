from __future__ import annotations

from typing import Any


def assert_subset(actual: dict[str, Any], expected: dict[str, Any], path: str = "") -> None:
    for key, exp in expected.items():
        p = f"{path}.{key}" if path else key
        assert key in actual, f"missing key {p}"
        act = actual[key]
        if isinstance(exp, dict) and isinstance(act, dict):
            assert_subset(act, exp, p)
        else:
            assert act == exp, f"{p}: expected {exp!r}, got {act!r}"
