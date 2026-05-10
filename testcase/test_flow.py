from __future__ import annotations

import pytest
import allure

from common.runner import run_case
from common.yaml_util import load_yaml


def _cases():
    doc = load_yaml("flow.yaml")
    return doc.get("cases") or []


@allure.epic("电商接口自动化")
@allure.feature("业务流程")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize("case", _cases(), ids=lambda c: str(c.get("name", "case")))
def test_yaml_flow(case: dict) -> None:
    allure.title(f"流程测试: {case.get('name', 'unnamed')}")
    run_case(case)
