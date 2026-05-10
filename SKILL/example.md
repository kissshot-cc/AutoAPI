# Examples

## 示例 1：梳理项目结构

### 用户输入
```text
请整体阅读这个 requests 接口测试项目，帮我整理项目结构、运行链路和当前风险点。
```

### 推荐输出结构
- 项目定位
- 目录树
- 模块职责
- 核心调用链
- 已实现能力
- 当前缺口

## 示例 2：写项目说明文档

### 用户输入
```text
请给这个接口测试项目补一份完整的项目说明文档，要求能用于交接。
```

### 推荐动作
1. 先阅读 `pytest.ini`、`conftest.py`、`common/request_util.py`
2. 再阅读 `api/`、`data/`、`testcase/`
3. 补充 `PROJECT_OVERVIEW.md`
4. 明确写出运行方式、扩展步骤、风险项

## 示例 3：复现一个同类项目

### 用户输入
```text
请参考这个项目，帮我复现一个 pytest + requests 的接口测试项目。
```

### 推荐输出
```text
我会优先搭建以下能力：
1. pytest 入口与 conftest 初始化
2. TokenManager 与 RequestUtil
3. BaseApi 和业务 API 分层
4. YAML 流程执行器
5. sqlite 初始化与断言
6. 完整流程测试与并发测试
```

## 示例 4：排查 token 失败

### 用户输入
```text
为什么这个支付接口一直 403？请帮我看 token 注入链路。
```

### 推荐检查顺序
1. `common/token_manager.py`
2. `common/request_util.py`
3. `conftest.py`
4. 目标 `api/*.py`
5. 是否存在 `no_token=True`
6. `Authorization` 是裸 token 还是 `Bearer token`

## 示例 5：补全 YAML 流程执行器

### 用户输入
```text
这个 runner.py 现在只是占位，帮我补成真正可执行 YAML 流程。
```

### 推荐实现目标
- 从 YAML 读取 steps
- 根据 `api` 找到对应函数
- 先做 `${var}` 替换
- 执行接口请求
- 按 `extract` 写入 `Context`
- 按 `assert` 做断言
- 失败时给出清晰报错

## 示例 6：给其他 agent 写 Prompt

### 用户输入
```text
帮我写一份专业 prompt，让其他 agent 能复现这个项目。
```

### 推荐 Prompt 结构
1. 项目目标
2. 技术栈
3. 目录约定
4. 核心能力
5. 验收标准
6. 交付内容
7. 实施顺序

## 示例 7：输出风险清单

### 用户输入
```text
请从测试架构角度 review 这个项目。
```

### 推荐关注点
- runner 是否为真实执行器
- API 方法是否混入测试逻辑
- 是否存在硬编码 base_url
- token 策略是否统一
- 并发用例是否有共享变量竞态
- DB 初始化是否足够稳定
