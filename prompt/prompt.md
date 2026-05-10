# Agent Reproduction Prompt

下面这份 Prompt 可以直接提供给其他 agent，用于复现当前 `APIAuto` 项目。

## 标准 Prompt

```text
你是一个专业的 Python 测试开发工程师。请复现一个本地运行的接口测试项目，项目形态参考一个基于 requests 的电商接口测试工程。

一、目标
请从零搭建一个可运行的 Python 接口测试项目，能够对本地电商服务进行接口验证，并满足以下两类测试能力：
1. 数据驱动的完整业务流测试
2. 并发下单/防超卖测试

二、技术栈与约束
1. 使用 Python
2. 使用 pytest 作为测试框架
3. 使用 requests 发送 HTTP 请求
4. 使用 allure 产出测试报告附件
5. 使用 yaml 管理测试数据/流程定义
6. 使用 sqlite 进行轻量数据库初始化与断言
7. 项目需能在本地运行，不依赖复杂外部基础设施

三、目录约定
项目至少包含以下目录和文件：

project_root/
├── api/
│   ├── base_api.py
│   ├── user_api.py
│   ├── product_api.py
│   ├── order_api.py
│   └── pay_api.py
├── common/
│   ├── request_util.py
│   ├── token_manager.py
│   ├── auth.py
│   ├── api_factory.py
│   ├── runner.py
│   ├── assert_util.py
│   ├── extract_util.py
│   ├── replace_util.py
│   ├── context.py
│   ├── yaml_util.py
│   ├── db_init.py
│   ├── db_util.py
│   └── db_assert.py
├── config/
│   ├── config.yaml
│   └── config_util.py
├── data/
│   └── flow.yaml
├── testcase/
│   ├── test_flow.py
│   └── test_oversell.py
├── conftest.py
└── pytest.ini

四、必须实现的核心能力

1. Token 自动登录与缓存
- 提供 TokenManager
- 支持 register_login(func)
- 支持 get_token() 获取并缓存 token
- 请求默认自动注入 token
- 注册/登录接口支持 no_token=True 跳过自动注入

2. 请求统一封装
- 用 RequestUtil 封装 requests.Session
- 统一处理 headers、token、请求发送、响应解析
- 自动将请求参数与响应内容附加到 allure

3. BaseApi 抽象
- 提供 BaseApi，负责拼接 base_url 和委托 RequestUtil
- 各业务 API 继承 BaseApi

4. API 分层
- UserApi：注册、登录
- ProductApi：新增商品
- OrderApi：创建订单
- PayApi：支付订单

5. YAML 数据驱动流程执行
- `data/flow.yaml` 中定义多步骤业务流
- 每个步骤支持：
  - api
  - data
  - extract
  - assert
- `common/runner.py` 必须真正执行每个 step，不能只打印占位内容

6. 上下文变量机制
- 支持通过 extract 从响应提取变量到 Context
- 支持 replace 将 `${var}` 替换为上下文值

7. 数据库初始化与断言
- 使用 sqlite
- 在 conftest 或 session 启动阶段自动建表
- 至少包含 products、orders 两张表
- 支持在测试中读取数据库并做断言

8. 并发超卖测试
- 编写 test_oversell.py
- 创建一个库存为 10 的商品
- 使用多线程并发创建订单
- 断言成功下单数不超过库存
- 断言库存不小于 0

五、测试流程要求

1. flow.yaml 至少覆盖以下业务链：
- 登录
- 新增商品
- 创建订单
- 支付

2. test_flow.py 需要参数化读取 flow.yaml 并执行

3. test_oversell.py 需要直接使用 Python 代码编排并发测试

六、配置要求
- `config.yaml` 至少包含：
  - base.url
  - user.username
  - user.password

七、工程质量要求
- 不允许只搭目录骨架，必须保证关键文件有可运行实现
- 不允许在业务方法中遗留递归式调试代码
- 不允许 runner.py 只返回 True 或只打印日志，必须真实执行 YAML 步骤
- 默认使用统一术语：API、token、context、extract、assert、flow
- 尽量保持模块职责单一

八、验收标准
请确保最终交付满足以下条件：
1. `python -m pytest` 可以执行
2. `pytest.ini` 支持生成 allure 结果目录
3. `test_flow.py` 能完成完整业务流
4. `test_oversell.py` 能执行并发超卖验证
5. token 自动获取与自动注入工作正常
6. YAML 变量提取和替换工作正常
7. sqlite 初始化和断言工作正常

九、交付内容
请输出：
1. 项目目录树
2. 核心模块说明
3. 关键代码实现
4. 运行命令
5. 已知限制或后续可优化点

十、实施建议
建议按以下顺序完成：
1. 写配置与 pytest 入口
2. 写 token 与 request_util
3. 写 BaseApi 和业务 API
4. 写 yaml/context/extract/replace/runner
5. 写 db 初始化与断言
6. 写 flow 测试
7. 写 oversell 并发测试
8. 自测并修正问题
```

## 企业级扩展 Prompt（可选）

如果需要让项目具备企业级特性，可在基础 Prompt 后追加以下内容：

```text
十一、企业级扩展要求

1. 多环境配置
- 支持 dotenv 加载 .env 文件
- config/env/ 目录下放置 dev.yaml / test.yaml / prod.yaml
- 环境变量优先级最高：环境变量 > env/<API_ENV>.yaml > config.yaml

2. 统一日志
- common/logger.py：RotatingFileHandler + token 掩码
- 支持 LOG_LEVEL 环境变量控制

3. 请求层增强
- 超时配置化（API_REQUEST_TIMEOUT）
- 重试机制（API_REQUEST_RETRIES，指数退避）
- ApiRequestError 自定义异常
- 日志中 token 必须掩码

4. Runner 增强
- 支持 setup / teardown 步骤
- 支持 when 条件跳过
- 支持 loop 循环展开
- 支持 soft_assert 软断言
- 支持 schema JSONSchema 校验

5. 提取增强
- extract_util 支持 JSONPath（$..id）

6. 数据工厂
- common/factory.py：Faker 生成唯一测试数据
- replace_util 支持 ${fake.xxx} 占位

7. 契约校验
- config/schemas/ 放置 JSONSchema 文件
- common/schema_util.py 提供 validate 函数

8. 测试分层
- pytest markers：smoke / regression / concurrency / integration
- test_flow.py 打 @pytest.mark.smoke + @pytest.mark.regression
- test_oversell.py 打 @pytest.mark.concurrency

9. Allure 元数据
- 用例添加 @allure.epic / @allure.feature / @allure.severity / @allure.title

10. CI/CD
- .github/workflows/ci.yml：lint + smoke/regression 分阶段

11. Mock 目录化
- mocks/ 目录按资源拆分路由

12. 工程化
- pyproject.toml：项目元数据 + 工具配置
- Makefile：一键命令
- Dockerfile + docker-compose.yml：容器化运行
- .pre-commit-config.yaml：代码质量钩子
```

## 使用建议
- 如果目标 agent 擅长代码生成，但不擅长架构收敛，可以直接附上本文件全文。
- 如果目标 agent 已经有现成项目，只想对齐结构，可只提供“目录约定 + 核心能力 + 验收标准”三部分。
- 如果目标 agent 是做代码评审/重构的，可在 Prompt 末尾追加企业级扩展部分。