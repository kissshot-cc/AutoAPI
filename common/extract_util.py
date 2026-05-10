from __future__ import annotations

from typing import Any

from common.context import Context

try:
    from jsonpath_ng.ext import parse as jsonpath_parse
    _HAS_JSONPATH = True
except ImportError:
    _HAS_JSONPATH = False


def _get_path(obj: Any, path: str) -> Any:
    """按路径取值：支持点号（a.b.c）和 JSONPath（$..id）。"""
    if path.startswith("$") and _HAS_JSONPATH:
        return _get_by_jsonpath(obj, path)

    cur: Any = obj
    for part in path.split("."):
        if part == "":
            continue
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


def _get_by_jsonpath(obj: Any, path: str) -> Any:
    """使用 JSONPath 提取。"""
    jsonpath_expr = jsonpath_parse(path)
    matches = jsonpath_expr.find(obj)
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0].value
    return [m.value for m in matches]


def extract(response: dict[str, Any], mapping: dict[str, str], ctx: Context) -> None:
    """
    mapping: context_key -> response path
    e.g. token -> token, pid -> data.id, ids -> $..id
    """
    for ctx_key, resp_path in mapping.items():
        ctx.set(ctx_key, _get_path(response, resp_path))
