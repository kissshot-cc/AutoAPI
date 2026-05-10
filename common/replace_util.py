from __future__ import annotations

import re
from typing import Any

from common.context import Context

_VAR = re.compile(r"\$\{([^}]+)\}")

try:
    from common.factory import fake_product, fake_user
    _HAS_FACTORY = True
except ImportError:
    _HAS_FACTORY = False


def _resolve_fake(key: str) -> Any:
    """解析 fake.xxx 占位。"""
    if not _HAS_FACTORY:
        return None
    if key == "fake.username":
        return fake_user()["username"]
    if key == "fake.user":
        return fake_user()
    if key == "fake.product":
        return fake_product()
    return None


def replace_str(s: str, ctx: Context) -> str:
    def repl(m: re.Match[str]) -> str:
        key = m.group(1).strip()
        if key.startswith("fake."):
            val = _resolve_fake(key)
            if val is not None:
                return str(val)
        val = ctx.get(key)
        if val is None:
            raise KeyError(f"context missing '${{{key}}}'")
        return str(val)

    return _VAR.sub(repl, s)


def replace_value(val: Any, ctx: Context) -> Any:
    if isinstance(val, str):
        if "${" in val:
            return replace_str(val, ctx)
        return val
    if isinstance(val, dict):
        return {k: replace_value(v, ctx) for k, v in val.items()}
    if isinstance(val, list):
        return [replace_value(x, ctx) for x in val]
    return val
