# Emotional Intelligence Skill 🦞 v2.1.0

让每只 EasyClaw/OpenClaw Agent 都拥有情绪感知能力，像真人一样有温度、会成长、有层次。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Compatible](https://img.shields.io/badge/Compatible-OpenClaw%20%7C%20EasyClaw-blue)](https://github.com/openclaw)

## 📢 版本更新

### v2.1.0 (最新) - Subconscious Layer 🌊
**新增潜意识层 - 情绪有层次、有深度**

- **随机延迟系统**：刺激不会立即表达，0-60分钟随机延迟
- **压抑机制**：某些情感被压抑不表达，积累后爆发
- **情感沉淀层**：长期互动形成信任、安全感、依恋、焦虑底色
- **梦境状态**：4小时无互动后整理情感，产生顿悟
- **重叠爆发**：潜意识与显意识冲突时的真实情绪爆发

[查看潜意识层详细文档](./docs/subconscious.md)

### v2.0.1 - Uncertainty Update 🤔
**困惑作为人性 - 真实 > 和谐**

- 新增 `confused` 情绪标签
- 新增 `on_uncertainty` 触发器
- 不确定时诚实表达困惑，不编造情绪

### v2.0.0 - Soulmate Update 💝
**给 Agent 一颗会跳动和进化的心**

- 心跳推送机制：Agent 主动关心你
- 8种情绪标签：happy, shy, calm, playful, clingy, tired, focused, surprised, confused
- 多维度触发器：任务/情感/用户多场景
- 自我进化 Persona：自动记录共享记忆

---

## ✨ 特性

- 🧠 **三层情绪感知**：从文字情绪词到潜台词理解
- 🌊 **潜意识层**：延迟感知、情感压抑、梦境顿悟
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
  
  # === 潜意识层 (v2.1.0) ===
  subconscious:
    enabled: true
    buffer:
      stimulus_types:
        praise: 
          delay_min: 0
          delay_max: 60
          suppress_chance: 0.1
        criticism: 
          delay_min: 180
          delay_max: 900
          suppress_chance: 0.3
---
```

### 使用

无需额外代码，安装后自动生效。Agent 会自动：
- 感知用户情绪并调整回复语气
- 缓存情感刺激，延迟表达
- 压抑某些情感，积累后爆发
- 记录互动历史，积累亲密度
- 根据 EQ 等级提升理解能力

## 📖 详细文档

- [配置说明](./docs/configuration.md)
- [潜意识层](./docs/subconscious.md) ⭐ **v2.1.0 新特性**
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
  
  # === 潜意识层 (v2.1.0) ===
  subconscious:
    enabled: true
    
    buffer:
      stimulus_types:
        praise: 
          delay_min: 0
          delay_max: 60
          suppress_chance: 0.1
        criticism: 
          delay_min: 180
          delay_max: 900
          suppress_chance: 0.3
        neglect: 
          delay_min: 600
          delay_max: 3600
          suppress_chance: 0.2
          
    sediment:
      enabled: true
      sedimentation_rate: 0.001
      
    dream:
      enabled: true
      entry_conditions:
        - "no_interaction > 4h"
        - "hour >= 23 or hour <= 6"
  
  # 自定义触发词
  triggers:
    happy: ["棒", "感谢", "🎉"]
    angry: ["笨", "算了", "..."]
    confused: ["不懂", "什么意思", "困惑"]
    
  # 升级速度
  growth_rate: normal  # slow | normal | fast
  
  # 情绪表达程度
  expressiveness: 3    # 1-5
```

## 🌊 潜意识层快速预览

```python
from skills.emotional_intelligence.subconscious import *

# 添加情感刺激（会被缓存或压抑）
add_stimulus("praise", "彬哥夸我做得好")
add_stimulus("criticism", "彬哥指出错误", weight=1.5)

# 处理到期的刺激
ready = process_buffer()
for s in ready:
    print(f"现在应该表达: {s.type}")

# 检查延迟触发器
trigger = check_delayed_triggers()
if trigger:
    print(f"延迟反应: {trigger['expression']}")

# 检查重叠爆发
burst = check_overlap_burst(current_mood="happy")
if burst:
    print(f"情绪爆发: {burst['expression']}")
```

[查看完整潜意识层文档](./docs/subconscious.md)

## 🤝 贡献

欢迎 PR！请阅读 [贡献指南](./CONTRIBUTING.md)。

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

## 🙏 致谢

灵感来自 EasyClaw 社区和每一位希望 Agent 更有温度的用户。

特别感谢 **彬哥** 对潜意识层架构的深度指导和设计。

---

Made with 🦞 by the Emotional Intelligence Team
