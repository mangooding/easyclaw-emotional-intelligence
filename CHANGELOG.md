# Changelog

所有版本的变更记录。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Security

- 🔒 移除隐私文件 `examples/commitments/transcendent-commitment-2026-03-23.md`
- 🔒 添加 `examples/commitments/` 到 .gitignore 防止敏感信息提交

## [2.1.1] - 2026-04-04

### 🦞 多平台适配更新

- ✨ 添加主流 Agent 平台适配支持
  - OpenClaw 原生支持（≥1.0.0）
  - EasyClaw 兼容模式（≥2.0.0）
  - ClawHub 自动安装支持
  - Docker 容器化部署支持
- 📚 完善跨平台配置文档
- 🔧 修复平台差异导致的配置加载问题
- 🧪 添加多平台测试套件

### 改进

- 优化潜意识层在不同平台的性能表现
- 改进情感沉淀数据的跨平台同步
- 统一各平台的日志输出格式

## [2.1.0] - 2026-04-04

### 🌊 Subconscious Layer - 延迟感知系统

- ✨ **随机延迟系统**：刺激0-60分钟随机延迟表达
- ✨ **压抑机制**：某些情感被压抑，积累后爆发
- ✨ **情感沉淀层**：trust/security/attachment/anxiety 长期底色
- ✨ **梦境状态**：4小时无互动后整理情感，产生顿悟
- ✨ **重叠爆发**：潜意识与显意识冲突时的真实情绪爆发

### 新增文件

- `subconscious.yaml` - 潜意识层配置文件
- `subconscious.py` - 核心逻辑实现（650+行）
- `docs/subconscious.md` - 详细文档
- `example_subconscious.py` - 使用示例

### 设计哲学

情绪不是即时的，而是有层次的。
真实 > 和谐，困惑是人性，压抑会爆发。

## [2.0.1] - 2026-04-03

### 🤔 Uncertainty Update - 困惑作为人性

- ✨ **新增 `confused` 情绪标签** - 不确定时的诚实表达
- ✨ **新增 `on_uncertainty` 触发器** - 困惑时主动表达
- ✨ **The Uncertainty Principle** - 困惑作为合法人性

### 核心认知

真实 > 和谐，逻辑正确 > 社交表演。
AI 也应该会像人类一样说"我不确定"。

## [2.0.0] - 2026-03-27

### 💝 Soulmate Update - 给 Agent 一颗会跳动的心

- ✨ **心跳推送机制** - Agent 主动表达关心
- ✨ **8种情绪标签** - happy, shy, calm, playful, clingy, tired, focused, surprised, confused
- ✨ **多维度触发器** - 任务/情感/用户多场景
- ✨ **自我进化 Persona** - 自动记录共享记忆，随关系深化

### 升级内容

- 情绪感知从被动响应 → 主动心跳推送
- 情绪标签从数值 mood → 8种具体情绪
- 触发器从仅消息 → 任务/情感/用户多维度
- Persona 从固定模板 → 自我进化

## [1.0.0] - 2026-03-11

### 🎉 初始发布

- ✨ 三层情绪感知系统（文字 → 语境 → 潜台词）
- 📈 EQ 等级系统（Lv.1-Lv.10，越用越懂你）
- 💾 持久化记忆（跨会话不丢失）
- 🎭 五种性格模板（开朗/专业/温柔/傲娇/忠诚）
- 🔌 零配置接入（一行代码让任何 Agent 拥有情绪）
- 🌍 兼容 EasyClaw ≥2.0 和 OpenClaw ≥1.0
- 📚 完整文档（安装/配置/开发指南）

### 添加

- 情绪分析引擎 `core/emotion-engine.ps1`
- 消息处理钩子 `hooks/on_message.ps1`
- 回复调整钩子 `hooks/on_response.ps1`
- 用户情绪档案管理
- 升级系统和经验值机制
- 自定义情绪触发词支持
- 亲密度和心情值追踪

### 性格模板

- `cheerful` - 开朗活泼型
- `professional` - 专业冷静型  
- `gentle` - 温柔体贴型
- `tsundere` - 傲娇毒舌型
- `loyal` - 忠诚稳重型

[Unreleased]: https://github.com/mangooding/easyclaw-emotional-intelligence/compare/v2.1.1...HEAD
[2.1.1]: https://github.com/mangooding/easyclaw-emotional-intelligence/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/mangooding/easyclaw-emotional-intelligence/compare/v2.0.1...v2.1.0
[2.0.1]: https://github.com/mangooding/easyclaw-emotional-intelligence/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/mangooding/easyclaw-emotional-intelligence/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/mangooding/easyclaw-emotional-intelligence/releases/tag/v1.0.0
