# 反模式清单

> 记录本项目历史上踩过的坑，供后续贡献者避雷。

---

## 1. base_url 硬编码

### 现象
`BaseApi` 中 `self.base_url = "http://127.0.0.1:5000"`

### 危害
无法切换环境，CI/测试环境无法运行

### 错误示例
```python
class BaseApi:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"  # ❌
```

### 正确做法
```python
class BaseApi:
    def __init__(self):
        self.base_url = get_base_url().rstrip("/")  # ✅
```

### 检测方式
```bash
grep -R "127.0.0.1" api/ common/
```

---

## 2. Runner 占位实现

### 现象
`runner.py` 的 `run_case()` 只 `print` 并返回 `True`

### 危害
YAML 用例永远不会被执行，测试形同虚设

### 错误示例
```python
def run_case(case):
    print(case["name"])  # ❌
    return True
```

### 正确做法
必须实现 `api` 分发、`data` 替换、`extract` 写入、`assert` 校验。

### 检测方式
运行 `pytest -v`，看 YAML 用例是否真正通过。

---

## 3. API 方法混入断言

### 现象
`ProductApi.add_product()` 中直接写 `assert resp["id"] > 0`

### 危害
API 层职责混淆，无法在其他场景复用

### 错误示例
```python
def add_product(self, name, stock, price):
    resp = self.request_util.post(...)
    assert resp["id"] > 0  # ❌
    return resp
```

### 正确做法
```python
def add_product(self, name, stock, price):
    return self.request_util.post(...)  # ✅

# testcase 中断言
def test_add():
    resp = api.add_product(...)
    assert resp["id"] > 0
```

---

## 4. Token 明文日志

### 现象
`logger.info(f"Headers: {headers}")` 打印完整 Authorization 头

### 危害
敏感信息泄露，日志文件可能落入他人手中

### 错误示例
```python
logger.info(f"Auth: Bearer {token}")  # ❌
```

### 正确做法
```python
logger.debug("Request headers: %s", masked_headers)  # ✅
# 或使用 MaskedFormatter 自动处理
```

### 检测方式
```bash
grep -R "Authorization.*Bearer" logs/
```

---

## 5. Context 跨用例污染

### 现象
`Context` 使用全局单例，多条用例共享

### 危害
用例不独立，执行顺序不同结果不同

### 错误示例
```python
# global context
global_ctx = Context()

def test_a():
    global_ctx.set("id", 1)

def test_b():
    assert global_ctx.get("id") == 1  # ❌ 依赖 test_a
```

### 正确做法
```python
def run_case(case):
    ctx = Context()  # ✅ 每条用例独立创建
```

---

## 6. 未清理 report/ 提交到 Git

### 现象
`.gitignore` 未忽略 `report/`，提交大量 allure JSON

### 危害
仓库体积膨胀，包含运行轨迹（hostname、执行时间）

### 检测方式
```bash
git ls-files report/ | wc -l
```

---

## 7. 缺少 markers 导致 CI 无法分阶段

### 现象
所有用例无标记，CI 只能全量跑

### 危害
PR 阶段等待时间过长

### 正确做法
```python
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.concurrency
```

---

## 8. YAML 中硬编码敏感数据

### 现象
`data/flow.yaml` 中 `password: admin123`

### 危害
代码仓库中明文密码

### 正确做法
使用环境变量或 Faker：
```yaml
password: ${TEST_PASSWORD}
username: ${fake.username}
```

---

## 9. 未设置 no_token 导致 401

### 现象
登录/注册接口默认带 token，被服务端拒绝

### 错误示例
```yaml
- api: user.login  # ❌ 未设 no_token
  data:
    username: admin
    password: admin123
```

### 正确做法
```yaml
- api: user.login
  no_token: true  # ✅
  data:
    username: admin
    password: admin123
```

---

## 10. Mock 与真实环境耦合过深

### 现象
`mock_server.py` 放在项目根，与业务代码同层

### 危害
目录结构混乱，不易维护

### 正确做法
```
mocks/
├── server.py
└── routes/
    ├── users.py
    ├── products.py
    ├── orders.py
    └── pay.py
```

---

## 检测脚本

```bash
#!/bin/bash
echo "=== 反模式扫描 ==="
echo "1. 硬编码 base_url:"
grep -Rn "127.0.0.1" api/ common/ --include="*.py" | grep -v "get_base_url"
echo "2. Runner 占位:"
grep -n "return True" common/runner.py
echo "3. API 混入断言:"
grep -Rn "assert " api/ --include="*.py"
echo "4. 未清理 report:"
git ls-files report/ | wc -l
echo "=== 扫描完成 ==="
```
