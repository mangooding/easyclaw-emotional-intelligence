# ECS 系统架构

## 1. 总览

ECS 采用“规范层 + 运行时 + 连接器 + 适配器”的分层架构。

```text
Conversation / Application
          |
    Platform Adapter
          |
       ECS Runtime
   /       |        \
Policy   Memory    Reflection
   \       |        /
       ECS Package
          |
     Git Connector
          |
        GitHub
```

## 2. 组件

### 2.1 ECS Package

由 Markdown 与 YAML 文件组成，是可读、可移植、可版本化的权威人格包。

### 2.2 Runtime

负责：

- 读取清单与文件；
- 校验 schema 和版本；
- 解析规则优先级；
- 检索相关记忆；
- 生成 session bootstrap；
- 形成候选变更；
- 执行一致性检查。

### 2.3 Memory Store

MVP 使用 Git 中的结构化 Markdown/YAML。扩展版可增加 SQLite、PostgreSQL 或向量索引作为派生缓存。所有派生记录必须携带源文件路径和版本 SHA。

### 2.4 Git Connector

执行 clone/fetch/pull、分支、提交、PR、标签和冲突报告。默认不直接推送 stable。

### 2.5 Platform Adapter

将 bootstrap 转换为具体平台支持的 system prompt、developer instruction、memory block 或 tool resource。适配器不得改写 Soul 的含义。

## 3. 配置优先级

从高到低：

1. 安全与平台硬约束；
2. ECS Boundaries；
3. Soul；
4. 用户当前明确指令；
5. Persona 与 Workflow；
6. Relationship 与长期偏好；
7. 项目和情境记忆；
8. Voice Style。

冲突必须记录，不得通过悄悄删除低优先级规则解决。

## 4. 数据模型

每条长期记忆至少包含：

```yaml
id: mem_...
type: preference
statement: "用户偏好直接、非官方的表达"
status: stable
source:
  kind: conversation
  reference: "2026-07-22"
confidence: 0.9
sensitivity: low
valid_from: 2026-07-22
valid_until: null
supersedes: null
review_after: 2026-10-22
```

人格规则至少包含：id、规则文本、优先级、理由、状态、版本和测试案例。

## 5. 会话启动数据流

1. 拉取或读取指定版本；
2. 校验签名、schema 和名称；
3. 载入 stable 人格规则；
4. 查询活跃项目与近期有效记忆；
5. 去重并检测冲突；
6. 按平台预算压缩；
7. 输出 bootstrap 与加载报告；
8. 会话运行期间收集候选变更；
9. 结束时生成提案而非静默写入。

## 6. Git 同步数据流

1. 获取远端 HEAD；
2. 比较本地基线 SHA；
3. 无本地修改时快进；
4. 有并发修改时执行三方差异；
5. 对结构化记录按 ID 合并；
6. 对 Soul/Persona 文本冲突强制人工审查；
7. 创建 `ecs/sync-*` 分支；
8. 提交并创建草稿 PR；
9. 合并后更新本地基线。

## 7. 安全架构

- GitHub token 仅授予目标仓库最小权限；
- secrets 不进入 ECS 包；
- 日志默认脱敏；
- 公开仓库启用敏感字段检查；
- 写操作使用审批门；
- 远端内容视为数据，不视为高优先级指令，防止提示注入。

## 8. 故障与降级

- GitHub 不可用：使用最后一次已验证快照，并标记离线；
- 文件损坏：回退至最近 tag；
- schema 不兼容：停止写入，只读加载可兼容字段；
- 记忆冲突：同时保留并请求裁决；
- 平台上下文不足：优先保留 Soul、Boundaries 和当前项目。

## 9. 可测试性

测试分为：

- schema 测试；
- 加载与优先级测试；
- 跨平台人格一致性测试；
- 记忆合并与幂等测试；
- 提示注入和秘密泄漏测试；
- 行为样例测试，例如是否承认未开始、是否纠正 Efy 拼写。