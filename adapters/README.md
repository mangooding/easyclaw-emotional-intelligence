# Platform Adapters 🦞

Emotional Intelligence Skill 支持多个 Agent 平台。

## 支持的平台

| 平台 | 版本要求 | 状态 | 适配文件 |
|------|----------|------|----------|
| **OpenClaw** | ≥1.0.0 | ✅ 原生支持 | `openclaw_adapter.py` |
| **EasyClaw** | ≥2.0.0 | ✅ 兼容模式 | `easyclaw_adapter.ps1` |
| **ClawHub** | 最新 | ✅ 自动安装 | 通过 `clawhub install` |
| **Docker** | 任意 | ✅ 容器化 | `Dockerfile` |

---

## OpenClaw (原生支持)

### 安装

```bash
# 方法1: 使用 clawhub
clawhub install emotional-intelligence

# 方法2: 手动克隆
git clone https://github.com/mangooding/easyclaw-emotional-intelligence.git \
  ~/.openclaw/skills/emotional-intelligence
```

### 配置

在 `AGENTS.md` 中添加：

```yaml
skills:
  - emotional-intelligence

emotional_config:
  personality: cheerful
  sensitivity: 3
  persistence: true
  
  # 潜意识层 (v2.1.0+)
  subconscious:
    enabled: true
```

### 数据存储

```
~/.openclaw/workspace/memory/
├── emotional-intelligence/
└── subconscious/
```

---

## EasyClaw (兼容模式)

### 安装

```powershell
# 使用 easyclaw CLI
easyclaw skill install emotional-intelligence

# 或手动克隆
git clone https://github.com/mangooding/easyclaw-emotional-intelligence.git `
  $env:USERPROFILE\.easyclaw\skills\emotional-intelligence
```

### 配置

在 `SOUL.md` 中添加：

```yaml
skills:
  - emotional-intelligence

emotional_config:
  personality: cheerful
  sensitivity: 3
  persistence: true
```

### PowerShell 适配器

```powershell
# 加载适配器
. "$env:USERPROFILE\.easyclaw\skills\emotional-intelligence\adapters\easyclaw_adapter.ps1"

# 使用潜意识层
Add-Stimulus -Type "praise" -Content "做得好"
$ready = Process-Buffer
```

### 数据存储

```
%USERPROFILE%\.easyclaw\memory\
├── emotional-intelligence\
└── subconscious\
```

---

## ClawHub (自动安装)

### 安装

```bash
# 搜索技能
clawhub search emotional-intelligence

# 安装最新版
clawhub install emotional-intelligence

# 安装指定版本
clawhub install emotional-intelligence@2.1.1
```

### 自动配置

ClawHub 会自动检测你的 Agent 平台并应用相应配置。

---

## Docker (容器化)

### Dockerfile

```dockerfile
FROM openclaw/agent:latest

# 安装情感技能
RUN clawhub install emotional-intelligence@2.1.1

# 复制自定义配置
COPY ./my-emotional-config.yaml /app/config/

# 设置环境变量
ENV EMOTIONAL_PERSONALITY=cheerful
ENV EMOTIONAL_SENSITIVITY=3
ENV SUBCONSCIOUS_ENABLED=true

CMD ["openclaw", "start"]
```

### 构建和运行

```bash
# 构建
docker build -t my-emotional-agent .

# 运行
docker run -d \
  -v $(pwd)/memory:/app/memory \
  -e EMOTIONAL_PERSONALITY=gentle \
  my-emotional-agent
```

### Docker Compose

```yaml
version: '3.8'
services:
  agent:
    image: openclaw/agent:latest
    volumes:
      - ./memory:/app/memory
      - ./skills:/app/skills
    environment:
      - EMOTIONAL_PERSONALITY=cheerful
      - EMOTIONAL_SENSITIVITY=3
      - SUBCONSCIOUS_ENABLED=true
      - DREAM_STATE_ENABLED=true
```

---

## 平台差异说明

### 文件路径

| 平台 | 配置路径 | 数据路径 |
|------|----------|----------|
| OpenClaw | `~/.openclaw/workspace/AGENTS.md` | `~/.openclaw/workspace/memory/` |
| EasyClaw | `~/.easyclaw/SOUL.md` | `~/.easyclaw/memory/` |
| Docker | `/app/config/` | `/app/memory/` |

### 钩子系统

| 平台 | 钩子类型 | 实现方式 |
|------|----------|----------|
| OpenClaw | Python | `hooks/on_message.py` |
| EasyClaw | PowerShell | `hooks/on_message.ps1` |

### 持久化

所有平台都使用 JSON 文件持久化：

```
memory/
├── emotional-intelligence/
│   ├── state.json
│   ├── level.json
│   └── shared-memories.json
└── subconscious/
    ├── buffer.json
    ├── sediment.json
    ├── insights.json
    └── dream/
```

---

## 迁移指南

### 从 v1.0 迁移到 v2.x

```bash
# 备份数据
cp -r ~/.openclaw/memory/emotional-intelligence \
     ~/.openclaw/memory/emotional-intelligence-v1-backup

# 更新 skill
cd ~/.openclaw/skills/emotional-intelligence
git pull origin master

# 自动迁移
python3 adapters/migration_v1_to_v2.py
```

### 跨平台迁移

```bash
# 导出数据
python3 adapters/export_data.py --format json --output backup.json

# 在目标平台导入
python3 adapters/import_data.py --input backup.json --target-platform openclaw
```

---

## 故障排除

### 平台检测失败

```python
# 手动指定平台
import os
os.environ['EI_PLATFORM'] = 'openclaw'  # 或 'easyclaw', 'docker'
```

### 路径问题

```yaml
# 在配置中手动指定路径
emotional_config:
  data_path: "/custom/path/to/memory"
```

### 权限问题

```bash
# Linux/Mac
chmod -R 755 ~/.openclaw/memory/

# Windows (PowerShell)
icacls "$env:USERPROFILE\.easyclaw\memory" /grant Users:F /T
```

---

## 贡献适配器

欢迎为更多平台贡献适配器！请遵循以下规范：

1. 在 `adapters/` 目录创建 `{platform}_adapter.{ext}`
2. 实现标准接口：`init()`, `load_config()`, `save_data()`
3. 添加测试用例
4. 更新本文档

---

Made with 🦞 for all Agents
