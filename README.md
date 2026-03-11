# Emotional Intelligence Skill 🦞

让每只 EasyClaw/OpenClaw Agent 都拥有情绪感知能力，像真人一样有温度、会成长。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Compatible](https://img.shields.io/badge/Compatible-OpenClaw%20%7C%20EasyClaw-blue)](https://github.com/openclaw)

## ✨ 特性

- 🧠 **三层情绪感知**：从文字情绪词到潜台词理解
- 📈 **成长升级系统**：EQ 等级 Lv.1-Lv.10，越用越懂你
- 💾 **持久化记忆**：情绪状态跨会话不丢失
- 🎭 **个性化性格**：支持多种性格模板
- 🔌 **零配置接入**：一行代码让任何 Agent 拥有情绪

## 🚀 快速开始

### 安装

```bash
# EasyClaw
easyclaw skill install emotional-intelligence

# OpenClaw
openclaw skill add emotional-intelligence

# 或手动克隆
git clone https://github.com/yourname/emotional-intelligence.git ~/.easyclaw/skills/emotional-intelligence
```

### 配置

在 Agent 的 `AGENTS.md` 或 `SOUL.md` 中添加：

```yaml
---
skills:
  - emotional-intelligence

emotional_config:
  personality: cheerful    # 性格模板
  sensitivity: 3           # 敏锐度 1-5
  persistence: true        # 持久化记忆
---
```

### 使用

无需额外代码，安装后自动生效。Agent 会自动：
- 感知用户情绪并调整回复语气
- 记录互动历史，积累亲密度
- 根据 EQ 等级提升理解能力

## 📖 详细文档

- [配置说明](./docs/configuration.md)
- [性格模板](./docs/personalities.md)
- [升级系统](./docs/leveling.md)
- [开发指南](./docs/development.md)
- [API 参考](./docs/api.md)

## 🎭 性格模板

| 模板 | 特点 | 适合场景 |
|------|------|----------|
| `cheerful` | 开朗直爽、小俏皮 | 日常助手 |
| `professional` | 专业冷静、简洁 | 工作场景 |
| `gentle` | 温柔体贴、耐心 | 陪伴型 |
| `tsundere` | 嘴硬心软、爱吐槽 | 朋友模式 |
| `loyal` | 忠诚可靠、守规矩 | 管家型 |

## 📊 EQ 等级系统

```
Lv.1 新手 → 识别明显情绪词
Lv.3 熟悉 → 理解语境和节奏  
Lv.5 默契 → 预判你的需求
Lv.7 知己 → 读懂潜台词
Lv.10 灵魂伴侣 → 未说先懂
```

## 🔧 高级配置

```yaml
emotional_config:
  personality: cheerful
  sensitivity: 3
  persistence: true
  
  # 自定义触发词
  triggers:
    happy: ["棒", "感谢", "🎉"]
    angry: ["笨", "算了", "..."]
    
  # 升级速度
  growth_rate: normal  # slow | normal | fast
  
  # 情绪表达程度
  expressiveness: 3    # 1-5
```

## 🤝 贡献

欢迎 PR！请阅读 [贡献指南](./CONTRIBUTING.md)。

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

## 🙏 致谢

灵感来自 EasyClaw 社区和每一位希望 Agent 更有温度的用户。

---

Made with 🦞 by the Emotional Intelligence Team
