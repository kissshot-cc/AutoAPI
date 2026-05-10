# 用例编写 Skill

## 触发场景

- 新增业务接口测试用例
- 编写回归/冒烟测试流程
- 补充并发/稳定性测试
- 维护 YAML 数据驱动用例

---

## 两种范式对比

| 维度 | YAML 数据驱动 | Python 代码编排 |
|------|--------------|----------------|
| 适用场景 | 标准业务流程 | 并发/复杂分支/DB 断言 |
| 维护者 | 测试工程师 | 测试开发 |
| 变量传递 | `${var}` + `extract` | 直接传参 |
| 断言方式 | `assert` 子集 | 自由 assert / db_assert |
| 示例 | `data/flow.yaml` | `testcase/test_oversell.py` |

---

## YAML 新增步骤 9 步法

1. **编写 API 方法**：在 `api/` 对应资源类中新增方法，只做路径/数据拼装
2. **注册 API 名称**：在 `common/api_factory.py` 的 `_REGISTRY` 中添加映射
3. **编写 YAML 步骤**：在 `data/flow.yaml` 的 `cases` 下追加 `steps`
4. **配置 extract**：从响应中提取后续需要的变量（如 `token`, `product_id`）
5. **配置 assert**：对响应做子集断言
6. **配置 schema**（可选）：引用 `config/schemas/` 中的 JSONSchema
7. **更新 Mock**：若使用本地 Mock，在 `mocks/routes/` 新增路由
8. **运行验证**：`pytest -v` 确认新用例通过
9. **检查清单**：确认 API 已注册、no_token 设置正确、变量名不冲突

### 示例

```yaml
cases:
  - name: register_and_login
    steps:
      - api: user.register
        data:
          username: ${fake.username}
          password: Test@123
        no_token: true
        assert:
          ok: true
        schema: register_response

      - api: user.login
        data:
          username: ${fake.username}
          password: Test@123
        no_token: true
        extract:
          token: token
```

---

## Python 用例模板

```python
from __future__ import annotations

import pytest
import allure
from api.xxx_api import XxxApi
from common.factory import fake_xxx
from common.db_assert import assert_xxx

@allure.epic("电商接口自动化")
@allure.feature("XXX 模块")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.regression
class TestXxx:

    @allure.story("XXX 操作")
    @allure.title("正常 XXX 场景")
    def test_xxx_happy_path(self):
        # 1. 准备测试数据
        data = fake_xxx()

        # 2. 调用 API
        api = XxxApi()
        resp = api.xxx_method(**data)

        # 3. 响应断言
        assert "id" in resp
        assert resp.get("ok") is True

        # 4. 数据库断言（可选）
        assert_xxx(resp["id"], expected_min=0)
```

---

## 命名规范

- **文件名**：`test_<资源>_<场景>.py`
- **类名**：`Test<资源>`（大驼峰）
- **方法名**：`test_<动作>_<场景>`（蛇形）
- **YAML case name**：`<业务域>_<流程名>`

示例：
- `test_order_create_flow.py`
- `TestProduct`
- `test_add_product_with_stock`
- `ecommerce_happy_path`

---

## 反模式清单

| 反模式 | 危害 | 正确做法 |
|--------|------|----------|
| 硬编码账号/商品名 | 数据冲突、无法并发 | 使用 `${fake.username}` / `fake_product()` |
| API 方法中写断言 | 职责混淆、无法复用 | API 只负责请求，断言在 testcase 中 |
| 跨用例共享 Context | 测试不独立、互相污染 | 每条用例独立 Context |
| 测不住的断言 | 假阳性/假阴性 | 断言必须有意义：状态码、关键字段、DB 状态 |
| 忘记 no_token | 401 报错 | 登录/注册接口必须设 `no_token: true` |

---

## 检查清单（提交前）

- [ ] API 方法已注册到 `api_factory._REGISTRY`
- [ ] YAML 步骤中 `api` 名称与注册名一致
- [ ] `${var}` 使用的变量已在前面步骤 `extract`
- [ ] 登录/注册步骤已设 `no_token: true`
- [ ] 并发用例使用 `@pytest.mark.concurrency`
- [ ] 用例包含 allure 装饰器（epic/feature/severity）
- [ ] 测试数据使用 Faker 而非硬编码
