# 项目优化 Skill

## 适用场景

当需要将一个原型接口测试项目升级为企业级测试框架时使用本 Skill。

---

## 评估矩阵

从以下 7 个维度对项目打分（1-5 分），识别薄弱环节：

| 维度 | 评分标准 | 当前状态 |
|------|---------|----------|
| 配置管理 | 是否支持多环境/环境变量覆盖 | ✅ 已完成（T-002） |
| 请求层 | 超时/重试/日志/异常/掩码 | ✅ 已完成（T-004） |
| Runner | setup/teardown/循环/条件/软断言 | ✅ 已完成（T-009） |
| 报告 | allure 分层/元数据/附件 | ✅ 已完成（T-007） |
| CI/CD | 自动化 lint/test/报告上传 | ✅ 已完成（T-005） |
| 质量 | ruff/black/mypy/coverage | ✅ 已完成（T-006/008） |
| SKILL | 用例编写/优化/反模式文档 | ✅ 已完成（T-020/021/022/023） |

---

## 优化优先级

### P0（必须优先完成）
- 统一配置 + 多环境支持
- 请求层超时/重试/日志/掩码
- CI 工作流（lint + test）
- SKILL 文档沉淀

### P1（核心能力提升）
- Allure 报告分层
- pytest 配置升级（markers/cov）
- Runner 增强（setup/teardown/loop）
- Faker 数据工厂
- JSONSchema 契约校验
- Mock 目录化

### P2（锦上添花）
- Docker 一键运行
- Makefile
- pyproject.toml 迁移
- pytest-rerunfailures/xdist 调参

---

## 落地顺序

参考 `SUGGESTIONS.md` 任务编号，推荐执行序：

```
T-001 (README)
T-002 (多环境配置)
T-003 (日志系统)
T-004 (RequestUtil 增强)
T-005 (GitHub Actions)
T-019 (requirements 分层)
T-017 (pyproject.toml)
T-007 (Allure 元数据)
T-008 (pytest 配置)
T-009 (Runner 增强)
T-010 (JSONPath)
T-011 (测试标记)
T-012 (Faker)
T-013 (JSONSchema)
T-014 (Mock 目录化)
T-016 (Makefile)
T-015 (Docker)
T-020~T-023 (SKILL 扩写)
```

---

## 验收模板

### 配置类优化
- [ ] `API_ENV=test` 可切换到对应环境
- [ ] 环境变量优先级高于 yaml
- [ ] 启动日志打印当前环境

### 代码类优化
- [ ] `pytest` 全量通过
- [ ] `ruff check .` 无错误
- [ ] 新增功能有对应测试覆盖

### 报告类优化
- [ ] allure 报告按 epic/feature 分组
- [ ] 每条用例有 severity 和 title
- [ ] 请求/响应附件正常显示

---

## 回滚策略

| 优化项 | 回滚方法 |
|--------|----------|
| 多环境配置 | 删除 `config/env/`，恢复 `config_util.py` 原版 |
| RequestUtil 增强 | 恢复原版 `request_util.py`，移除 retry/timeout 依赖 |
| Runner 增强 | 恢复原版 `runner.py`，仅保留基础 step 执行 |
| pyproject.toml | 删除 `pyproject.toml`，恢复 `pytest.ini` |
| Mock 目录化 | 恢复 `mock_server.py` 为单体，删除 `mocks/` |

回滚后必须重新运行 `pytest` 验证。
