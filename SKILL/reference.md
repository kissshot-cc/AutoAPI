# Reference

## 参考项目画像
这个 Skill 参考的是一个本地电商接口测试工程，关键特征如下：

- 测试框架：`pytest`
- 请求库：`requests`
- 报告：`allure`
- 数据驱动：`yaml`
- 状态校验：`sqlite`
- 分层结构：`api + common + testcase + data + config`

## 标准模块职责定义

### `pytest.ini`
负责：
- pytest 默认参数
- allure 结果目录
- Python 路径

### `conftest.py`
负责：
- session 级初始化
- 自动建表
- 注册默认登录函数
- 初始化 token

### `common/request_util.py`
负责：
- 持有 `requests.Session`
- 自动注入 token
- 统一发送请求
- 记录/附加请求响应
- 返回 JSON 结果

### `common/token_manager.py`
负责：
- 保存缓存 token
- 接收登录函数
- 在无 token 时自动登录并缓存

### `api/base_api.py`
负责：
- 持有 `RequestUtil`
- 拼接 `base_url + path`
- 为资源 API 提供统一入口

### `api/*.py`
负责：
- 一种资源一个类
- 一种接口一个方法
- 方法只关注路径、method、json、params、headers

### `common/context.py`
负责：
- 在多步骤流程中保存运行时变量

### `common/extract_util.py`
负责：
- 从响应中提取字段到 `Context`

### `common/replace_util.py`
负责：
- 把 `${var}` 替换成上下文值

### `common/runner.py`
理想职责：
- 顺序执行 YAML 里的每个 step
- 调用对应 API
- 替换输入变量
- 提取输出变量
- 做断言

### `common/db_*.py`
负责：
- 初始化 sqlite 表
- 直接查询测试数据库
- 做状态断言

## 推荐的分析问题
阅读一个 requests 接口测试项目时，优先回答这些问题：

1. 这个项目如何启动？
2. token 从哪里来？
3. 哪些请求默认带 token？
4. API 层和测试层是如何解耦的？
5. YAML 是否只是数据，还是已经形成可执行 DSL？
6. 数据库存在哪些场景下被拿来验结果？
7. 项目哪些部分已经落地，哪些部分还是骨架？

## 推荐的文档章节
给此类项目写文档时，优先包含：

### 1. 项目定位
说明这是功能验证型接口项目、流程回归项目，还是并发/稳定性项目。

### 2. 目录结构
给出 2-3 层目录树即可，重点突出 `api/ common/ testcase/ data/ config/`。

### 3. 调用链
建议使用 mermaid 表达：
- `pytest -> conftest -> token/db init`
- `testcase -> runner/api -> request_util -> target service`
- `extract/replace/context` 在链路中的位置

### 4. 已实现能力
只列已经在代码中真实存在的能力。

### 5. 缺口与风险
例如：
- 占位实现
- 硬编码
- 调试残留
- 格式不统一
- 可扩展性不足

### 6. 扩展步骤
告诉后续维护者怎么加一个新接口、一个新 YAML 步骤、一个新 DB 断言。

## 参考检查清单

### 阅读项目时
- [ ] 找到启动入口
- [ ] 找到 token 注入位置
- [ ] 找到 BaseApi
- [ ] 找到 API 工厂/映射
- [ ] 找到 YAML 文件
- [ ] 找到 runner 实现
- [ ] 找到数据库初始化逻辑
- [ ] 找到并发或特殊业务测试

### 复现项目时
- [ ] 先搭配置和 pytest 入口
- [ ] 再做 token + request_util
- [ ] 再做 BaseApi + 业务 API
- [ ] 再做 context/extract/replace/runner
- [ ] 再做数据库初始化与断言
- [ ] 再做流程测试与并发测试
- [ ] 最后自测并清理调试残留

## 常见误区
- 只写 `testcase`，不写 `common/request_util.py`
- 有 YAML 文件，但没有真正执行 YAML 的 runner
- 在 API 方法里直接写测试逻辑
- 只做接口返回断言，不做状态回查
- token 管理分散在多个文件中，导致难维护
