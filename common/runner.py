from __future__ import annotations

from copy import deepcopy
from typing import Any

import allure

from common.api_factory import dispatch
from common.assert_util import assert_subset
from common.context import Context
from common.extract_util import extract
from common.replace_util import replace_value
from common.schema_util import validate as validate_schema
from common.soft_assert import clear_failures, get_failures, raise_if_any, soft_assert
from common.token_manager import TokenManager


def _eval_when(when_expr: str, ctx: Context) -> bool:
    """简单条件表达式求值：${var} == 'value' / ${var} > 0。"""
    expr = replace_value(when_expr, ctx)
    if isinstance(expr, bool):
        return expr
    try:
        return bool(eval(str(expr), {"__builtins__": {}}, {}))
    except Exception:
        return False


def _run_step(i: int, step: dict[str, Any], ctx: Context, *, soft_mode: bool = False) -> None:
    """执行单个步骤。"""
    api_name = step.get("api")
    if not api_name:
        raise ValueError(f"step {i}: missing api")

    raw_data = step.get("data") or {}
    data = replace_value(raw_data, ctx)
    no_token = bool(step.get("no_token", False))

    with allure.step(f"{i + 1}. {api_name}"):
        resp = dispatch(api_name, data, no_token=no_token)

        if "extract" in step:
            mapping = step["extract"]
            if not isinstance(mapping, dict):
                raise TypeError("extract must be a dict")
            extract(resp, mapping, ctx)
            tok = ctx.get("token")
            if tok is not None:
                TokenManager.set_token(str(tok))

        if "schema" in step:
            validate_schema(resp, step["schema"])

        if "assert" in step:
            expected = replace_value(step["assert"], ctx)
            if soft_mode or step.get("soft_assert"):
                try:
                    assert_subset(resp, expected)
                except AssertionError as e:
                    soft_assert(False, str(e))
            else:
                assert_subset(resp, expected)


def run_case(case: dict[str, Any], base_context: dict[str, Any] | None = None) -> None:
    name = case.get("name") or "unnamed"
    with allure.step(f"case: {name}"):
        ctx = Context()
        if base_context:
            ctx.update(dict(base_context))

        # Setup 阶段
        for i, step in enumerate(case.get("setup") or []):
            _run_step(i, step, ctx)

        steps = case.get("steps") or []
        for i, step in enumerate(steps):
            # 条件跳过
            when_expr = step.get("when")
            if when_expr and not _eval_when(when_expr, ctx):
                continue

            # 循环展开
            loop = step.get("loop")
            if loop is not None:
                if isinstance(loop, int):
                    items = range(loop)
                elif isinstance(loop, list):
                    items = loop
                else:
                    items = replace_value(loop, ctx)
                    if isinstance(items, int):
                        items = range(items)

                for idx, item in enumerate(items):
                    loop_ctx = deepcopy(ctx)
                    loop_ctx.set("item", item)
                    loop_ctx.set("index", idx)
                    loop_step = replace_value(step, loop_ctx)
                    _run_step(i, loop_step, loop_ctx, soft_mode=bool(step.get("soft_assert")))
                    ctx.update(loop_ctx.data)
            else:
                _run_step(i, step, ctx, soft_mode=bool(step.get("soft_assert")))

        # 软断言汇总
        failures = get_failures()
        if failures:
            msg = "\n".join(f"  - {f}" for f in failures)
            raise AssertionError(f"Soft assertions failed ({len(failures)} issues):\n{msg}")

        # Teardown 阶段（即使失败也执行）
        for i, step in enumerate(case.get("teardown") or []):
            try:
                _run_step(i, step, ctx)
            except Exception:
                pass  # teardown 失败不阻断报告
