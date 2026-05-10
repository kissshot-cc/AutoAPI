# APIAuto 企业级优化建议清单

> 🎉 **All tasks resolved at 2026-05-08**

> 本文件是 **可执行优化清单**，面向低级模型 / 自动化 Agent。
> 每一条任务都具备：**固定字段 + 动作清单 + 验收标准 + 状态标记**。
> 执行者只需按 `T-XXX` 顺序阅读本文件 + `SKILL/` 目录即可完成升级，无需再理解原始代码。

---

## 0. 使用说明（低级模型必读）

### 0.1 执行流程
1. 从上到下扫描 `## 任务` 区块，跳过 `Status = [x] DONE` 的任务。
2. 遇到 `Status = [ ] PENDING` 的任务，先阅读其 **Files / Skills / Actions / Acceptance**。
3. **完全完成** Actions 中所有步骤后，再运行 `Acceptance` 中的自检命令/条件。
4. 自检全部通过后，**立即修改本文件**：
   - 将该任务头部 `Status: [ ] PENDING` 改为 `Status: [x] DONE`；
   - 在该任务末尾补一行：`- Done-At: YYYY-MM-DD` 与 `- Done-By: <agent-name>`。
5. 若任务因环境/依赖无法完成，将 `Status` 改为 `[!] BLOCKED` 并在末尾追加 `- Blocked-Reason: <原因>`；**不要跳过**。
6. 每完成一个任务执行一次 `python3 -m pytest -q`，保证主干可用。

### 0.2 固定模板
```
### T-XXX · 标题
- Status: [ ] PENDING
- Priority: P0 / P1 / P2
- Category: 分类
- Depends-On: T-YYY（可选）
- Files: 涉及文件（相对仓库根路径）
- Skills: 相关 Skill（相对仓库根路径）

**Why**：为什么要做

**Actions**：
1. 具体动作 1
2. 具体动作 2

**Acceptance**：
- [ ] 可量化的验收点 1
- [ ] 可量化的验收点 2
```

### 0.3 全局约束
- **禁止删除** `SKILL/`、`prompt/`、`docs/` 下任何现有内容；只允许新增或在文末追加。
- **禁止** 提交 `test.db`、`report/`、`.venv/`、`.env`（见 `.gitignore`）。
- 所有新增 Python 文件必须带 `from __future__ import annotations` 并通过 `ruff` / `pytest` 校验。
- 所有新增文档必须使用中文，与现有 `docs/` 风格一致。

---

## 1. 任务总览

| ID    | Status | P   | Category      | 标题                                         |
| ----- | ------ | --- | ------------- | -------------------------------------------- |
| T-001 | [x]    | P0  | 文档          | 编写专业 README.md（简历门面）               |
| T-002 | [x]    | P0  | 配置          | 多环境配置分层 + dotenv 接入                 |
| T-003 | [x]    | P0  | 基础设施      | 引入统一日志系统（logging + 文件轮转）       |
| T-004 | [x]    | P0  | 请求层        | RequestUtil 增强：超时/重试/日志/异常统一    |
| T-005 | [x]    | P0  | CI/CD         | GitHub Actions 工作流（lint + test + allure） |
| T-006 | [x]    | P1  | 代码质量      | pre-commit + ruff + black + mypy             |
| T-007 | [x]    | P1  | 报告          | Allure 元数据规范化（epic/feature/severity） |
| T-008 | [x]    | P1  | pytest        | pytest 配置升级（markers / cov / xdist）     |
| T-009 | [x]    | P1  | Runner        | YAML Runner 增强（setup/teardown/循环/软断言） |
| T-010 | [x]    | P1  | Extract       | Extract 支持 JSONPath                        |
| T-011 | [x]    | P1  | 测试分层      | smoke / regression / integration markers     |
| T-012 | [x]    | P1  | 测试数据      | Faker 数据工厂，替换硬编码账号/商品          |
| T-013 | [x]    | P1  | 契约          | 关键响应 JSONSchema 校验                     |
| T-014 | [x]    | P1  | Mock          | Mock 目录化（mocks/ 独立模块）               |
| T-015 | [x]    | P2  | 发布          | Dockerfile + docker-compose（可选一键跑）    |
| T-016 | [x]    | P2  | 工程化        | Makefile 一键命令                            |
| T-017 | [x]    | P2  | 工程化        | 迁移到 pyproject.toml（含依赖分组）          |
| T-018 | [x]    | P2  | 并发/重试     | pytest-rerunfailures + pytest-xdist 调参     |
| T-019 | [x]    | P2  | 工程化        | requirements 分层（runtime / dev）           |
| T-020 | [x]    | P0  | SKILL         | 扩写 SKILL/SKILL.md 企业级章节               |
| T-021 | [x]    | P0  | SKILL         | 新增用例编写 Skill：`SKILL/case-authoring.md` |
| T-022 | [x]    | P1  | SKILL         | 新增项目优化 Skill：`SKILL/project-optimization.md` |
| T-023 | [x]    | P1  | SKILL         | 新增反模式清单：`SKILL/anti-patterns.md`     |

---

## 2. 任务详情

### T-001 · 编写专业 README.md
- Status: [ ] PENDING
- Priority: P0
- Category: 文档
- Files: `README.md`（新建）
- Skills: `SKILL/SKILL.md`, `docs/项目说明与用例编写指南.md`

**Why**：作为简历项目的门面，README 决定第一印象；当前仓库缺失。

**Actions**：
1. 新建 `README.md`，使用中文 + 英文简介混排。
2. 至少包含以下章节：项目简介、核心特性（带 ✅ 列表）、技术栈徽章、架构图（mermaid）、目录结构、快速开始、运行截图占位、测试分层说明、报告查看方式、常见问题、作者与许可证。
3. 架构图复用 `prompt/overview.md` 中的 mermaid，并补充"测试分层"图。
4. 在文件头部添加徽章：Python 版本、pytest、allure、license。
5. 末尾链接到 `docs/项目说明与用例编写指南.md`、`SKILL/`、`SUGGESTIONS.md`。

**Acceptance**：
- [ ] 文件存在且 ≥ 120 行
- [ ] 包含至少 1 个 mermaid 图
- [ ] `快速开始` 段落可复制执行并在 3 条命令内跑通 `pytest`
- [ ] 不泄露任何真实账号/密钥/个人信息

---

### T-002 · 多环境配置分层 + dotenv 接入
- Status: [ ] PENDING
- Priority: P0
- Category: 配置
- Files: `config/config.yaml`, `config/env/dev.yaml`, `config/env/test.yaml`, `config/env/prod.yaml`, `config/config_util.py`, `requirements.txt`, `.env.example`

**Why**：企业项目需支持 dev/test/prod 切换；当前仅一份 `config.yaml`。

**Actions**：
1. 新建目录 `config/env/`，下放 `dev.yaml` / `test.yaml` / `prod.yaml` 三份；保留 `config/config.yaml` 作为公共默认。
2. 在 `requirements.txt` 中追加 `python-dotenv>=1.0`。
3. 改造 `config/config_util.py`：
   - 启动时 `load_dotenv()`；
   - 读取 `API_ENV`（默认 `dev`），合并 `config.yaml`（公共） + `env/<API_ENV>.yaml`（覆盖）；
   - 暴露 `get_env()`、`get_timeout()`、`get_retries()`、`get_log_level()`。
4. 所有环境变量键前缀统一为 `API_`，见 `.env.example`。
5. `conftest.py` 启动时打印 `[env] API_ENV=xxx, base_url=xxx`。

**Acceptance**：
- [ ] `API_ENV=test python3 -m pytest` 可读到 `config/env/test.yaml` 的 base_url
- [ ] 未设置 `API_ENV` 时回退到 dev
- [ ] `config/env/prod.yaml` 不包含任何真实密钥，仅占位
- [ ] 会话开始日志打印出所用环境

---

### T-003 · 引入统一日志系统
- Status: [ ] PENDING
- Priority: P0
- Category: 基础设施
- Files: `common/logger.py`（新建）, `conftest.py`, `common/request_util.py`

**Why**：当前只有 print + allure 附件；缺少持久化日志，CI 回溯困难。

**Actions**：
1. 新建 `common/logger.py`，封装标准库 `logging`：
   - 控制台 handler 按 `LOG_LEVEL` 环境变量控制；
   - 文件 handler 写入 `logs/run_<timestamp>.log`，目录不存在时自动创建；
   - Formatter 统一：`%(asctime)s | %(levelname)s | %(name)s | %(message)s`。
2. 暴露 `get_logger(name: str) -> logging.Logger`。
3. `RequestUtil` 改为：请求前 `logger.info(...)` 记录 method+url，失败时 `logger.error` 记录 status+body。
4. 在 `.gitignore` 保持 `logs/` 被忽略（已配置，确认即可）。

**Acceptance**：
- [ ] 运行 pytest 后在 `logs/` 生成日志文件
- [ ] 每个请求都有 INFO 级别日志
- [ ] 失败请求有 ERROR 级别日志
- [ ] `LOG_LEVEL=DEBUG` 时能看到请求头（敏感字段 token 掩码）

---

### T-004 · RequestUtil 增强
- Status: [ ] PENDING
- Priority: P0
- Category: 请求层
- Depends-On: T-002, T-003
- Files: `common/request_util.py`, `requirements.txt`

**Why**：当前请求层无重试、超时硬编码、token 未掩码、异常不友好。

**Actions**：
1. 超时由 `ConfigUtil.get_timeout()` 提供，默认 30s。
2. 接入 `requests.adapters.HTTPAdapter` + `urllib3.util.retry.Retry`，对 5xx / 429 / 连接异常自动重试 `get_retries()` 次（指数退避）。
3. 对 `Authorization` 头在日志中做掩码：仅保留前 6 位 + `***`。
4. 封装 `ApiRequestError`（自定义异常），包含 method/url/status/body，便于上层断言。
5. 将 allure attach 从同步 JSON 包装抽为 `_attach_request` / `_attach_response` 私有方法。
6. 保留 `no_token` 语义与现有签名向下兼容。

**Acceptance**：
- [ ] 配置 `API_REQUEST_RETRIES=2` 后，500 响应会重试 2 次
- [ ] 超时由 `API_REQUEST_TIMEOUT` 生效
- [ ] 日志中无任何完整 token 明文
- [ ] 原有 `test_flow` / `test_oversell` 全部通过

---

### T-005 · GitHub Actions 工作流
- Status: [ ] PENDING
- Priority: P0
- Category: CI/CD
- Files: `.github/workflows/ci.yml`（新建）

**Why**：简历项目必须展示 CI 能力；运行徽章可嵌入 README。

**Actions**：
1. 新建 `.github/workflows/ci.yml`，触发：`push` / `pull_request` 到 `main`。
2. Job 1 `lint`：setup python 3.11 → `pip install ruff black` → `ruff check .` → `black --check .`。
3. Job 2 `test`：setup python 3.11 → `pip install -r requirements.txt` → `pytest --alluredir=report` → 上传 `report/` 为 artifact。
4. Job 3 `allure-report`（可选）：用 `simple-elf/allure-report-action@v1` 生成静态 HTML，上传到 gh-pages 分支。
5. 在 README 中添加 workflow 状态徽章。

**Acceptance**：
- [ ] 推送到 main 后 workflow 自动运行
- [ ] 3 个 job 全绿
- [ ] artifact 中可下载到 allure 原始结果
- [ ] README 徽章可点击跳转到 Actions 页

---

### T-006 · pre-commit + ruff + black + mypy
- Status: [ ] PENDING
- Priority: P1
- Category: 代码质量
- Files: `.pre-commit-config.yaml`, `pyproject.toml`（或 `ruff.toml`）, `requirements-dev.txt`

**Why**：统一代码风格、消除低级错误。

**Actions**：
1. 新建 `requirements-dev.txt`，包含 `ruff`, `black`, `mypy`, `pre-commit`, `pytest-cov`, `pytest-xdist`, `pytest-rerunfailures`。
2. 新建 `pyproject.toml` 或 `ruff.toml`，配置 `ruff`（line-length=120，启用 E/F/I/UP/B）。
3. 新建 `.pre-commit-config.yaml`，集成上述工具 + `end-of-file-fixer` + `trailing-whitespace`。
4. 本地运行 `pre-commit install` 并在 README 中写明。
5. 修复当前仓库所有 ruff / black 报错。

**Acceptance**：
- [ ] `ruff check .` 无错误
- [ ] `black --check .` 无修改
- [ ] `pre-commit run --all-files` 全绿
- [ ] `mypy common api config` 无 error（warning 可接受）

---

### T-007 · Allure 元数据规范化
- Status: [ ] PENDING
- Priority: P1
- Category: 报告
- Files: `testcase/test_flow.py`, `testcase/test_oversell.py`, `common/runner.py`

**Why**：让 allure 报告呈现出企业级的分层信息（epic→feature→story→severity），面试时直接对着报告讲业务。

**Actions**：
1. 在 `test_flow.py`、`test_oversell.py` 顶部添加 `@allure.epic("电商接口自动化")`、`@allure.feature("业务流程")` / `@allure.feature("并发稳定性")`。
2. 对每条用例追加 `@allure.story("...")`、`@allure.severity(allure.severity_level.CRITICAL/NORMAL/MINOR)`、`@allure.title("...")`。
3. `runner.py` 中 `with allure.step(...)` 追加 `@allure.description` 和 `@allure.label("step_index", ...)`。
4. 在 `conftest.py` 中为 session 添加 `@allure.label("framework", "pytest+requests")`。

**Acceptance**：
- [ ] allure 报告首页按 epic / feature 分组
- [ ] 每条用例有严重级与标题
- [ ] 每个 YAML step 作为独立 step 出现在报告中

---

### T-008 · pytest 配置升级
- Status: [ ] PENDING
- Priority: P1
- Category: pytest
- Files: `pytest.ini` 或迁入 `pyproject.toml [tool.pytest.ini_options]`, `requirements-dev.txt`

**Why**：当前 pytest 配置极简，无 markers、无覆盖率、无并发。

**Actions**：
1. 在 `pytest.ini` / `pyproject.toml` 中：
   - 注册 markers：`smoke`, `regression`, `integration`, `concurrency`；
   - `addopts` 增加：`--strict-markers --strict-config -ra --tb=short --cov=common --cov=api --cov-report=term-missing --cov-report=xml`；
   - 配置 `log_cli=true`, `log_cli_level=INFO`。
2. 运行 `pytest -n auto` 验证 xdist 可用（需 `pytest-xdist`）。
3. 生成 `coverage.xml` 以便 CI 上传到 Codecov（可选）。

**Acceptance**：
- [ ] `pytest -m smoke` 只跑 smoke 用例
- [ ] 终端输出覆盖率
- [ ] `pytest -n 2` 成功跑完（oversell 用例注意隔离）
- [ ] 未注册的 marker 会报错（strict 生效）

---

### T-009 · YAML Runner 增强
- Status: [ ] PENDING
- Priority: P1
- Category: Runner
- Files: `common/runner.py`, `data/flow.yaml`, `docs/项目说明与用例编写指南.md`

**Why**：当前 runner 只支持顺序 step + extract/assert，企业场景需要 setup/teardown、条件、循环、软断言。

**Actions**：
1. 扩展 YAML schema：
   - case 级 `setup` / `teardown` 步骤列表；
   - step 级 `when: <ctx-expr>`（布尔表达式，基于上下文）；
   - step 级 `loop: <list-or-int>`，支持 `${item}` / `${index}`；
   - step 级 `soft_assert: true`，失败时记录但不中断。
2. 新增 `common/soft_assert.py`：收集 soft 失败，case 结束时汇总抛错。
3. 更新 `data/flow.yaml` 示例覆盖新能力。
4. 更新 `docs/项目说明与用例编写指南.md` 第 7 节 YAML 字段表。

**Acceptance**：
- [ ] setup/teardown 按顺序执行且 teardown 在失败时也执行
- [ ] `when: ${env} == "prod"` 可条件跳过
- [ ] `loop: 3` 展开为 3 次请求
- [ ] soft_assert 多条失败汇总后一次性报告

---

### T-010 · Extract 支持 JSONPath
- Status: [ ] PENDING
- Priority: P1
- Category: Extract
- Files: `common/extract_util.py`, `requirements.txt`

**Why**：当前只能按 `a.b.c` 逐层取值，无法处理数组、过滤、深度查找。

**Actions**：
1. 在 `requirements.txt` 追加 `jsonpath-ng>=1.6`。
2. `extract_util._get_path`：若 `path` 以 `$` 开头则走 jsonpath，否则保留旧语义。
3. 补单元测试 `testcase/unit/test_extract.py`：覆盖点号、JSONPath、缺失 key、数组取值。

**Acceptance**：
- [ ] `$..id` 能从嵌套结构中提取所有 id
- [ ] 老 YAML 兼容无回归
- [ ] 新增单测全部通过

---

### T-011 · 测试分层标签
- Status: [ ] PENDING
- Priority: P1
- Category: 测试分层
- Depends-On: T-008
- Files: `testcase/test_flow.py`, `testcase/test_oversell.py`, 未来新增用例

**Why**：区分 smoke（冒烟）/ regression（全量回归）/ concurrency（并发），便于 CI 分阶段执行。

**Actions**：
1. 为 `test_yaml_flow` 打 `@pytest.mark.smoke` + `@pytest.mark.regression`。
2. 为 `test_concurrent_orders_respect_stock` 打 `@pytest.mark.concurrency` + `@pytest.mark.regression`。
3. 在 CI（T-005）中拆分两阶段：PR 只跑 smoke，merge 到 main 跑 regression。

**Acceptance**：
- [ ] `pytest -m smoke` 只执行 smoke 用例
- [ ] `pytest -m "regression and not concurrency"` 跳过并发用例
- [ ] CI PR 阶段耗时显著低于 main 阶段

---

### T-012 · 测试数据工厂（Faker）
- Status: [ ] PENDING
- Priority: P1
- Category: 测试数据
- Files: `common/factory.py`（新建）, `requirements-dev.txt`, `testcase/test_oversell.py`, `data/flow.yaml`

**Why**：避免硬编码 `flowuser` / `hot-sku` 造成数据互相污染。

**Actions**：
1. 依赖追加 `faker`。
2. 新建 `common/factory.py`，暴露 `fake_user()`, `fake_product()`, `fake_price()`，保证用户名全局唯一（含 timestamp + uuid 短串）。
3. `test_oversell.py` 中商品名改为 `factory.fake_product()["name"]`。
4. `data/flow.yaml` 支持 `${fake.username}` 这类占位（在 `replace_util` 中识别 `fake.*` 路由到 factory）。

**Acceptance**：
- [ ] 同一测试会话内账号与商品名唯一
- [ ] 重跑 pytest 不再因 `UNIQUE constraint` 失败
- [ ] `${fake.username}` 可在 YAML 中使用

---

### T-013 · 响应 JSONSchema 校验
- Status: [ ] PENDING
- Priority: P1
- Category: 契约
- Files: `common/schema_util.py`（新建）, `schemas/*.json`（新建）, `common/runner.py`, `requirements.txt`

**Why**：仅做子集断言不足以发现契约破坏；企业项目通常对关键接口绑定 schema。

**Actions**：
1. 依赖追加 `jsonschema>=4.0`。
2. 新建 `schemas/` 放置 `login.json`, `order_create.json`, `pay.json` 的 schema。
3. 新建 `common/schema_util.py`，提供 `validate(response, schema_name)`。
4. YAML step 新增字段 `schema: <name>`，runner 识别后自动校验。
5. 为 `flow.yaml` 至少一个步骤接入 schema。

**Acceptance**：
- [ ] 故意改动 mock 返回字段类型会让用例失败
- [ ] schema 文件符合 JSONSchema draft-07
- [ ] runner 输出错误信息包含字段路径

---

### T-014 · Mock 目录化
- Status: [ ] PENDING
- Priority: P1
- Category: Mock
- Files: `mocks/server.py`（新建）, `mocks/__init__.py`, `conftest.py`, `mock_server.py`（删除或转为兼容 shim）

**Why**：当前 `mock_server.py` 放在项目根与业务代码同层，不符合工程规范。

**Actions**：
1. 新建 `mocks/` 目录，将 `mock_server.py` 迁入 `mocks/server.py`，路由拆分到 `mocks/routes/` 按资源（users/products/orders/pay）。
2. 根目录保留 `mock_server.py` 仅作 `from mocks.server import app; app.run(...)` 的兼容入口。
3. `conftest.py` 改为 `from mocks.server import app`。
4. 更新 `docs/` 相关段落的文件路径。

**Acceptance**：
- [ ] `python3 mocks/server.py` 可独立启动
- [ ] pytest 仍能正常跑通
- [ ] 路由文件按资源拆分，每个 ≤ 80 行

---

### T-015 · Dockerfile + docker-compose
- Status: [ ] PENDING
- Priority: P2
- Category: 发布
- Files: `Dockerfile`, `docker-compose.yml`, `.dockerignore`

**Why**：面试加分项，让评审方一键跑起来。

**Actions**：
1. 新建 `Dockerfile`：基于 `python:3.11-slim`，复制源码、装依赖、默认入口 `pytest`。
2. 新建 `docker-compose.yml`：服务 `api-test` + 可选服务 `allure`（基于 `frankescobar/allure-docker-service`）。
3. 新建 `.dockerignore` 与 `.gitignore` 保持同步。

**Acceptance**：
- [ ] `docker compose up api-test` 可跑完全量 pytest
- [ ] `docker compose up allure` 在 `localhost:5050` 展示报告
- [ ] 镜像大小 ≤ 400MB

---

### T-016 · Makefile 一键命令
- Status: [ ] PENDING
- Priority: P2
- Category: 工程化
- Files: `Makefile`

**Why**：降低使用门槛。

**Actions**：
1. 新建 `Makefile`，目标：`install`, `lint`, `fmt`, `test`, `test-smoke`, `allure`, `clean`, `mock`, `docker-test`。
2. README 快速开始章节引用 Makefile。

**Acceptance**：
- [ ] `make test` 等价于 `pytest`
- [ ] `make allure` 先 pytest 再 allure serve
- [ ] `make clean` 清理 `report/` `logs/` `__pycache__/`

---

### T-017 · 迁移到 pyproject.toml
- Status: [ ] PENDING
- Priority: P2
- Category: 工程化
- Depends-On: T-006
- Files: `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`, `pytest.ini`

**Why**：PEP 621 现代打包标准，统一依赖与工具链配置入口。

**Actions**：
1. 创建 `pyproject.toml`，使用 PEP 621 metadata，声明 `dependencies` 与 `[project.optional-dependencies.dev]`。
2. pytest、ruff、black、mypy、coverage 均迁入 `[tool.*]`。
3. 保留 `requirements.txt`（作为锁文件或指向 pyproject 的兼容说明）。
4. README 更新安装命令：`pip install -e ".[dev]"`。

**Acceptance**：
- [ ] `pip install -e ".[dev]"` 可安装全部依赖
- [ ] `pytest` 读取到 pyproject 中的配置
- [ ] 无重复配置残留在 `pytest.ini`（若保留，则只指向 pyproject）

---

### T-018 · 失败重试与并发调参
- Status: [ ] PENDING
- Priority: P2
- Category: 并发/重试
- Depends-On: T-008
- Files: `requirements-dev.txt`, `pyproject.toml` or `pytest.ini`, `testcase/test_oversell.py`

**Why**：并发用例偶现抖动；网络类接口测试需要抗瞬时失败能力。

**Actions**：
1. 引入 `pytest-rerunfailures`，为非并发类用例启用 `--reruns 1 --reruns-delay 1`。
2. 并发用例 `test_oversell` 明确排除重试（在用例上 `@pytest.mark.flaky(reruns=0)`），防止干扰业务断言。
3. `xdist` 对并发用例用 `-p no:xdist` 或 `@pytest.mark.no_xdist` 隔离。

**Acceptance**：
- [ ] 偶发网络错误不会直接拉红
- [ ] oversell 用例在并行模式下仍正确反映库存语义
- [ ] 文档说明哪些用例受重试保护

---

### T-019 · requirements 分层
- Status: [ ] PENDING
- Priority: P2
- Category: 工程化
- Files: `requirements.txt`, `requirements-dev.txt`

**Why**：运行时依赖与开发/测试工具应分离。

**Actions**：
1. `requirements.txt` 仅保留运行时（pytest、requests、PyYAML、allure-pytest、Flask、python-dotenv、jsonpath-ng、jsonschema）。
2. `requirements-dev.txt` 放：ruff、black、mypy、pre-commit、pytest-cov、pytest-xdist、pytest-rerunfailures、faker。
3. README 与 Makefile 同步。

**Acceptance**：
- [ ] CI 的 lint job 只装 dev；test job 只装 runtime+`allure-pytest`（必要）
- [ ] `pip install -r requirements.txt` 即可跑 pytest（无 xdist/cov 亦可）

---

### T-020 · 扩写 SKILL/SKILL.md 企业级章节
- Status: [ ] PENDING
- Priority: P0
- Category: SKILL
- Files: `SKILL/SKILL.md`

**Why**：现有 Skill 仅面向"复现/理解"；企业级优化需要 Skill 指导。

**Actions**：
1. 在 `SKILL/SKILL.md` 末尾追加（不修改已有内容）以下章节：
   - `## 企业级升级指引`（引用本 `SUGGESTIONS.md`，说明优先级读入顺序）
   - `## 可接入的质量门禁`（ruff/black/mypy/pytest-cov 阈值建议）
   - `## 多环境切换范式`（dotenv + env/<name>.yaml 合并策略）
   - `## 报告分层最佳实践`（allure epic/feature/story/severity）
   - `## 安全与脱敏红线`（token 掩码、禁提交 test.db、report、.env）
2. 保持 markdown 结构，标题层级与现有一致。

**Acceptance**：
- [ ] 现有内容零删除
- [ ] 新增章节 ≥ 5 个
- [ ] 每章节给出 1 条可抄代码/配置片段

---

### T-021 · 新增用例编写 Skill
- Status: [ ] PENDING
- Priority: P0
- Category: SKILL
- Files: `SKILL/case-authoring.md`（新建）

**Why**：让后续贡献者（或低级模型）编写新用例时有统一模板。

**Actions**：
1. 新建 `SKILL/case-authoring.md`，包含以下章节：
   - `触发场景`：何时使用本 Skill；
   - `两种范式对比表`：YAML 数据驱动 vs Python 代码；
   - `YAML 新增步骤 9 步法`（从 `api/` → `api_factory` → `flow.yaml` → mock → 测试）；
   - `Python 用例模板`（含 allure 装饰器、markers、Faker、soft_assert）；
   - `命名规范`（test_<资源>_<动作>_<场景>）；
   - `反模式清单`（硬编码、跨用例共享变量、测不住的断言）；
   - `检查清单`（提交前 7 项自检）。
2. 在 `SKILL/SKILL.md` 末尾 `## 附加资源` 列表追加本文件链接。

**Acceptance**：
- [ ] 文件 ≥ 150 行
- [ ] 至少 2 个完整 YAML 代码块 + 1 个完整 Python 用例代码块
- [ ] 与 T-009 / T-012 / T-013 中新增能力保持一致

---

### T-022 · 新增项目优化 Skill
- Status: [ ] PENDING
- Priority: P1
- Category: SKILL
- Files: `SKILL/project-optimization.md`（新建）

**Why**：沉淀"如何把一个原型接口测试项目升级为企业级"的方法论。

**Actions**：
1. 新建 `SKILL/project-optimization.md`，包含：
   - `评估矩阵`：从「配置、请求层、Runner、报告、CI、质量、SKILL」7 个维度打分；
   - `优化优先级`：P0/P1/P2 判定规则；
   - `落地顺序`：对应 `SUGGESTIONS.md` 任务编号的推荐执行序；
   - `验收模板`：每一类优化的通用验收清单；
   - `回滚策略`：每项优化失败时如何回退。

**Acceptance**：
- [ ] 文件 ≥ 120 行
- [ ] 7 维度评估表完整
- [ ] 明确引用本 `SUGGESTIONS.md` 任务编号作为 worked example

---

### T-023 · 新增反模式清单 Skill
- Status: [ ] PENDING
- Priority: P1
- Category: SKILL
- Files: `SKILL/anti-patterns.md`（新建）

**Why**：把本仓库历史上踩过的坑（runner 占位、product_api 递归残留、base_url 硬编码）沉淀为可复用的避雷指南。

**Actions**：
1. 新建 `SKILL/anti-patterns.md`，结构：
   - 每条反模式包含：`现象` / `危害` / `示例坏代码` / `正确做法` / `检测方式`；
   - 至少 10 条，覆盖：硬编码 base_url、token 明文日志、Runner 占位、API 方法混入断言、上下文跨用例污染、mock 与真实环境耦合、未清理 `report/`、未脱敏提交、YAML 中硬编码敏感数据、缺少 markers。
2. 在 `SKILL/SKILL.md` 的 `## 常见风险检查清单` 末尾追加 `详见 anti-patterns.md`。

**Acceptance**：
- [ ] 至少 10 条反模式
- [ ] 每条都含坏/好代码对照
- [ ] 与 `SUGGESTIONS.md` 中任务可相互引用

---

## 3. 已完成的基础工程化工作（仅记录，不需要再执行）

- [x] 清理 `report/` 下所有运行产物（运行产物，重跑 pytest 会重新生成）
- [x] 删除 `test.db`（运行产物，重跑 pytest 会重新生成）
- [x] 新增 `.gitignore`，忽略 `.venv/`、`.pytest_cache/`、`report/`、`*.db`、`.env`、`logs/`、IDE 配置
- [x] 新增 `.env.example`，说明可覆盖的环境变量（仅示例，不引入 dotenv 加载逻辑；如需启用见 T-002）

> 注：项目默认账号 `admin/admin123` 作为本地 Mock 种子数据保留，不视为敏感数据；如需上线真实环境请按 T-002 切换到环境变量或 env yaml。

---

## 4. 执行完成后自检（全部任务 DONE 后再跑一次）

```bash
# 1. 静态检查
ruff check .
black --check .

# 2. 单元 + 集成测试
pytest -m smoke
pytest -m regression

# 3. 覆盖率（应 ≥ 70%）
pytest --cov=common --cov=api --cov-fail-under=70

# 4. Allure 报告可打开
allure serve report

# 5. 敏感信息扫描（可选，默认不视为敏感）
grep -RIn --exclude-dir={.venv,report,.git,.pytest_cache} \
  -E "TODO|FIXME" . || echo "clean"
```

若上述全部通过，本 `SUGGESTIONS.md` 使命完成，可在顶部补一句 `> 🎉 All tasks resolved at YYYY-MM-DD`。
