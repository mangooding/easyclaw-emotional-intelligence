# 配置说明

## 基础配置

在 `AGENTS.md` 或 `SOUL.md` 顶部添加：

```yaml
---
skills:
  - emotional-intelligence

emotional_config:
  personality: cheerful      # 性格模板
  sensitivity: 3             # 敏锐度 1-5
  persistence: true          # 持久化记忆
  expressiveness: 3          # 情绪表达程度
  growth_rate: normal        # 升级速度
---
```

## 配置项详解

### personality (性格模板)

| 值 | 描述 | 适合场景 |
|-----|------|----------|
| `cheerful` | 开朗活泼，带点小俏皮 | 日常助手、朋友模式 |
| `professional` | 专业冷静，简洁高效 | 工作场景、商务助理 |
| `gentle` | 温柔体贴，耐心关怀 | 陪伴型、情感支持 |
| `tsundere` | 嘴硬心软，爱吐槽 | 轻松氛围、朋友互怼 |
| `loyal` | 稳重可靠，恭敬尽责 | 管家型、服务型 |

### sensitivity (敏锐度)

控制情绪检测的敏感程度：

- `1` - 迟钝：只识别明显的情绪词
- `2` - 适中：识别常见情绪表达
- `3` - 标准（推荐）：平衡敏感度和准确度
- `4` - 敏锐：能捕捉细微情绪变化
- `5` - 极敏：对语气和用词高度敏感

### persistence (持久化)

是否跨会话保存情绪状态：

- `true`（推荐）：情绪状态和记忆持久保存
- `false`：每次会话重置

### expressiveness (表达程度)

控制情绪表达的外显程度：

- `1` - 内敛：情绪变化几乎不表现出来
- `2` - 含蓄：轻微的情绪表达
- `3` - 自然（推荐）：适度的情绪表达
- `4` - 外放：明显的情绪表达
- `5` - 奔放：强烈的情绪表达

### growth_rate (升级速度)

控制 EQ 等级提升的速度：

- `slow` - 慢速：需要更多互动才能升级
- `normal`（推荐）：正常速度
- `fast` - 快速：更容易升级

## 高级配置

### 自定义情绪触发词

```yaml
emotional_config:
  custom_triggers:
    happy: ["太棒了", "完美", "绝了", "🎉", "👍"]
    angry: ["笨蛋", "算了", "...", "无语"]
    tired: ["先这样", "明天", "累了", "困"]
    worried: ["不对", "有问题", "检查下"]
    sad: ["难过", "伤心", "遗憾", "😢"]
    excited: ["激动", "期待", "终于", "wow"]
```

### 完全自定义示例

```yaml
---
name: 我的专属助手
personality: cheerful
skills:
  - emotional-intelligence
  - web-search
  - file-manager

emotional_config:
  personality: tsundere           # 傲娇性格
  sensitivity: 4                  # 敏锐一点
  persistence: true               # 记住我
  expressiveness: 4               # 情绪外放一点
  growth_rate: fast               # 快速成长
  
  custom_triggers:
    happy: ["牛逼", "6", "绝了", "爱了"]
    angry: ["笨", "傻", "无语", "服了"]
    
  # 称呼设置（可选）
  preferred_title: "老大"         # 亲昵称呼
  formal_title: "您"              # 正式称呼
---

你好老大！今天有什么吩咐？😤
```

## 多 Agent 配置

可以为不同 Agent 设置不同性格：

```yaml
# 工作助理
---
name: 工作小助手
skills:
  - emotional-intelligence
emotional_config:
  personality: professional
  sensitivity: 2
---

# 生活助理
---
name: 生活小管家
skills:
  - emotional-intelligence
emotional_config:
  personality: gentle
  sensitivity: 4
---

# 损友模式
---
name: 阿杰
skills:
  - emotional-intelligence
emotional_config:
  personality: tsundere
  sensitivity: 3
---
```

## 配置优先级

配置按以下优先级加载：

1. 当前消息中的配置（最高）
2. Agent 的 `AGENTS.md` 配置
3. 全局默认配置（最低）

## 故障排除

### 配置不生效
- 检查 YAML 格式是否正确
- 确保 `skills:` 列表中包含 `emotional-intelligence`
- 重启 Agent 或会话

### 想重置配置
```bash
# 删除记忆文件
rm ~/.easyclaw/memory/emotional-intelligence/state_*.json
```

### 切换性格不生效
- 清空记忆后重新加载
- 或使用 `setPersonality()` API 动态切换
