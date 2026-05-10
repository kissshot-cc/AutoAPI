name: requests-api-test-project
description: Analyze, reconstruct, document, or extend Python API test projects built with pytest and requests. Use when the user asks to梳理接口测试项目、复现 requests 测试工程、补全 token/请求封装/YAML 流程执行、或为类似项目编写结构说明与运行文档。
---

# Requests API Test Project

## 适用场景
在以下情况优先使用本 Skill：

- 用户要求阅读、梳理、总结一个 Python 接口测试项目
- 用户要求复现一个 `pytest + requests` 风格的测试工程
- 用户要求补全 token 管理、请求封装、YAML 数据驱动流程
- 用户要求为接口测试工程撰写结构文档、说明文档、交接文档
- 用户要求新增接口、补充流程测试、排查 token/鉴权/上下文替换问题

## 快速检查顺序
遇到类似项目时，按这个顺序阅读：

1. `pytest.ini`
2. `conftest.py`
3. `common/request_util.py`
4. `common/token_manager.py`
5. `api/base_api.py`
6. `api/*.py`
7. `common/context.py`
8. `common/extract_util.py`
9. `common/replace_util.py`
10. `common/runner.py`
11. `data/*.yaml`
12. `testcase/*.py`
13. `common/db_init.py` / `common/db_util.py` / `common/db_assert.py`

## 标准分析框架

### 1. 先确认入口
- `pytest` 从哪里启动
- `conftest.py` 做了哪些 session 初始化
- 是否自动建表、自动登录、自动准备 token

### 2. 再确认鉴权
- token 是如何获取的
- 是否有 `register_login()` / `get_token()`
- 哪些接口需要跳过 token 注入
- `Authorization` 格式是裸 token 还是 `Bearer token`

### 3. 再确认请求层
- 是否统一封装在 `RequestUtil`
- 是否使用 `requests.Session`
- 是否统一处理日志、Allure、异常、重试

### 4. 再确认 API 分层
- 是否有 `BaseApi`
- 各接口是否按资源拆分到独立类
- API 方法是否只做路径/数据拼装，不混入测试逻辑

### 5. 再确认流程驱动能力
- 是否存在 `data/*.yaml`
- `runner.py` 是否真的执行 `api/data/extract/assert`
- 是否支持 `${var}` 替换和响应提取

### 6. 再确认状态校验能力
- 是否有 DB 初始化和断言
- 是否有业务侧并发测试或状态回查测试

## 输出模板
当用户要求“梳理项目”或“写说明文档”时，优先输出以下结构：

1. 项目定位
2. 目录树
3. 模块职责
4. 核心运行链路
5. 已实现能力
6. 当前缺口与风险
7. 扩展一个新接口/新用例的步骤
8. 运行方式

## 复现类任务的默认要求
如果用户要求“复现一个类似项目”，默认要求包含：

- `pytest`
- `requests`
- `allure`
- `yaml`
- `sqlite`
- `TokenManager`
- `RequestUtil`
- `BaseApi`
- `api/ common/ testcase/ data/ config/` 目录
- 数据驱动完整流程测试
- 并发超卖测试

## 常见风险检查清单
- `runner.py` 是占位实现，只打印日志不执行真实逻辑
- API 方法里残留调试代码或递归调用自身
- `base_url` 硬编码，没有真正走配置
- token 注入格式与服务端要求不一致
- `Context` 被多个测试污染但没有清理策略
- 数据驱动步骤定义了 `extract/assert`，执行器却没有支持

## 交付建议
- 简单问题：给出结构说明和定位结论
- 中等复杂度：补一份 `PROJECT_OVERVIEW.md`
- 需要长期复用：再补一份 agent Prompt 和 Skill

## 附加资源
- 参考实现说明见 [reference.md](reference.md)
- 示例提示词见 [examples.md](examples.md)
- 用例编写规范见 [case-authoring.md](case-authoring.md)
- 项目优化方法论见 [project-optimization.md](project-optimization.md)
- 反模式清单见 [anti-patterns.md](anti-patterns.md)

## 企业级升级指引

当需要将本项目从原型升级为企业级测试框架时，优先阅读 `SUGGESTIONS.md` 并按 P0/P1/P2 顺序执行。
关键路径：配置统一 → 请求层增强 → CI → 质量门禁 → 报告分层 → SKILL 沉淀。

## 可接入的质量门禁

| 工具 | 阈值建议 | 配置位置 |
|------|---------|----------|
| ruff | 0 error, 0 warning | `pyproject.toml [tool.ruff]` |
| black | 0 diff | `.pre-commit-config.yaml` |
| mypy | 0 error（warning 可接受） | `pyproject.toml [tool.mypy]` |
| pytest-cov | ≥ 70% | `pyproject.toml [tool.coverage.report]` |

## 多环境切换范式

```bash
# 开发环境（默认）
pytest

# 测试环境
API_ENV=test pytest

# 生产环境（CI 中由环境变量注入）
API_ENV=prod API_BASE_URL=https://api.example.com pytest
```

合并策略：`config.yaml`（公共）→ `config/env/<API_ENV>.yaml`（覆盖）→ 环境变量（最高优先）。

## 报告分层最佳实践

```python
@allure.epic("电商接口自动化")
@allure.feature("订单流程")
@allure.story("创建订单")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("正常创建订单")
def test_create_order(): ...
```

Allure 报告首页按 epic → feature → story 三级分组，severity 用于过滤。

## 安全与脱敏红线

- Token 在日志中必须掩码（仅保留前 6 位 + `***`）
- 禁止提交 `test.db`、`report/`、`.env`（见 `.gitignore`）
- 配置文件中的默认账号仅限 Mock 环境，生产环境必须用环境变量覆盖
- 详见 [anti-patterns.md](anti-patterns.md) 中「敏感信息泄露」条目
