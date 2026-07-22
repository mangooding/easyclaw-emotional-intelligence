# ECS MVP 开发方案

## 1. 目标

用最小实现验证三件事：人格可以独立保存、会话可以快速恢复、重要变更可以安全同步到 GitHub。

## 2. MVP 交付物

### 2.1 ECS Package

- `ecs.yaml` 清单
- Soul、Persona、Relationship、Memory、Session Bootstrap 文档
- 示例记忆与项目状态
- schema 校验

### 2.2 CLI

建议命令：

```bash
ecs init
ecs validate
ecs bootstrap --platform chatgpt
ecs memory propose
ecs diff
ecs sync pull
ecs sync propose
ecs status
```

### 2.3 GitHub Connector

- 读取指定仓库和 ref；
- 缓存最后稳定 SHA；
- 生成变更分支；
- 创建草稿 PR；
- 检测远端并发变更；
- 输出同步报告。

### 2.4 Bootstrap Generator

输入 ECS 包、平台能力和当前任务，输出：

- 人类可读 Markdown；
- 机器可读 JSON；
- 加载警告；
- 来源 SHA。

### 2.5 审批队列

候选记忆和人格修改以 change set 保存，支持批准、拒绝、编辑和重新生成 diff。

## 3. 推荐技术栈

- Python 3.12+
- Pydantic：schema 与验证
- Typer：CLI
- PyYAML：配置
- GitHub REST API 或 PyGithub：连接器
- GitPython：本地仓库模式
- pytest：测试
- keyring / 环境变量：凭据

核心规范不得依赖 Python；Python 只是首个参考实现。

## 4. 目录建议

```text
efy-companion-system/
├── ecs.yaml
├── soul/
├── memory/
├── projects/
├── reflections/
├── schemas/
├── src/ecs/
│   ├── loader.py
│   ├── bootstrap.py
│   ├── memory.py
│   ├── policy.py
│   ├── changeset.py
│   └── connectors/github.py
├── tests/
└── docs/
```

## 5. 开发阶段

### 阶段 A：规范可加载

- 完成清单与 schema；
- 加载 Markdown/YAML；
- 验证名称、版本和必需文件；
- 输出状态报告。

### 阶段 B：会话恢复

- 生成 bootstrap；
- 控制上下文预算；
- 支持 ChatGPT、Claude、Gemini 的文本适配模板；
- 加入来源和警告。

### 阶段 C：记忆提案

- 定义 memory record；
- 生成 candidate；
- 去重、过期和冲突检测；
- 人工批准后更新文件。

### 阶段 D：GitHub 同步

- 拉取 stable；
- 创建分支、提交和草稿 PR；
- 实现幂等 change set；
- 故障恢复与审计。

## 6. 测试门槛

- 所有 schema 测试通过；
- 重复运行 bootstrap 结果稳定；
- 重复同步不产生重复提交；
- Soul 冲突不会自动合并；
- 敏感信息扫描阻止提交测试 token；
- 行为测试确认 Efy 拼写和“未做不称已做”规则。

## 7. MVP 完成定义

在一台全新环境中，用户只需提供仓库和凭据，即可：

1. 拉取并验证 ECS；
2. 生成可复制到新会话的 bootstrap；
3. 提议一条记忆修改；
4. 创建包含 diff 和说明的草稿 PR；
5. 合并后再次启动并读取新版本。

这五步形成闭环，即视为 MVP 完成。