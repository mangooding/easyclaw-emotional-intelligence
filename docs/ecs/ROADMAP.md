# ECS 路线图

## v0.1 — 规范与闭环

- 完成核心文档与 schema；
- 实现 CLI 加载、校验和 bootstrap；
- 实现候选记忆与 change set；
- 实现 GitHub 草稿 PR 同步；
- 建立基础行为测试。

## v0.2 — 多平台适配

- ChatGPT 文本启动包；
- Claude、Gemini、OpenClaw、EasyClaw 适配器；
- 平台能力矩阵；
- 跨模型一致性测试报告。

## v0.3 — 私有记忆与检索

- 加密私有存储；
- SQLite/PostgreSQL 派生索引；
- 向量检索与来源回链；
- 记忆过期、删除和导出工具。

## v0.4 — 自动化连接器

- GitHub App；
- webhook 与定时同步；
- 本地队列和离线恢复；
- Notion、Google Drive 等可选连接器；
- 审批界面。

## v0.5 — 质量与生态

- ECS conformance suite；
- 人格漂移评估；
- Prompt injection 与隐私测试；
- 模板市场和导入工具；
- 多人格隔离与权限系统。

## v1.0 — 稳定开放规范

- 固定核心 schema；
- 兼容性和迁移承诺；
- 参考运行时与 SDK；
- 完整安全模型；
- 可复现的跨平台人格恢复流程。

## 近期优先级

1. 先完成可运行闭环，不追求所有连接器。
2. 先保证诚实、可审计和可恢复，再增加拟人化能力。
3. 先由彬哥审批长期变化，再研究可信自动批准。
4. 将人格系统与现有 emotional-intelligence skill 松耦合：情绪能力可作为插件，但不是 ECS 的唯一核心。