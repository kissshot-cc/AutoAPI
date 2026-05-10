from __future__ import annotations

from typing import Any

_failures: list[str] = []


def soft_assert(condition: bool, message: str) -> None:
    """记录软断言失败，不中断执行。"""
    if not condition:
        _failures.append(message)


def get_failures() -> list[str]:
    return list(_failures)


def clear_failures() -> None:
    _failures.clear()


def raise_if_any() -> None:
    """如果有软断言失败，汇总抛出 AssertionError。"""
    if _failures:
        msg = "\n".join(f"  - {f}" for f in _failures)
        raise AssertionError(f"Soft assertions failed ({len(_failures)} issues):\n{msg}")
