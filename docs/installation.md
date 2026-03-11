# 安装指南

## EasyClaw 市场安装

### 方法 1：命令行安装（推荐）

```bash
# 搜索技能
easyclaw skill search emotional-intelligence

# 安装
easyclaw skill install emotional-intelligence

# 安装特定版本
easyclaw skill install emotional-intelligence@1.0.0

# 更新
easyclaw skill update emotional-intelligence

# 卸载
easyclaw skill uninstall emotional-intelligence
```

### 方法 2：配置文件安装

在 `~/.easyclaw/config.yaml` 中添加：

```yaml
skills:
  marketplace:
    - emotional-intelligence
```

然后运行：
```bash
easyclaw sync
```

## OpenClaw 市场安装

### 方法 1：命令行安装

```bash
# 添加技能
openclaw skill add emotional-intelligence

# 从 GitHub 直接添加
openclaw skill add https://github.com/easyclaw/emotional-intelligence

# 更新
openclaw skill update emotional-intelligence
```

### 方法 2：配置安装

在 `~/.openclaw/skills.yaml` 中添加：

```yaml
skills:
  - name: emotional-intelligence
    source: marketplace
    version: latest
```

## 手动安装

### 步骤 1：克隆仓库

```bash
# 进入 skills 目录
cd ~/.easyclaw/skills

# 克隆仓库
git clone https://github.com/easyclaw/emotional-intelligence.git

# 或者下载解压
wget https://github.com/easyclaw/emotional-intelligence/archive/refs/tags/v1.0.0.tar.gz
tar -xzf v1.0.0.tar.gz
mv emotional-intelligence-1.0.0 emotional-intelligence
```

### 步骤 2：验证安装

```bash
# 检查技能列表
easyclaw skill list

# 应该能看到 emotional-intelligence
```

### 步骤 3：配置 Agent

在 Agent 的 `AGENTS.md` 中添加：

```yaml
---
skills:
  - emotional-intelligence

emotional_config:
  personality: cheerful
---
```

## 验证安装

安装完成后，可以通过以下方式验证：

### 1. 检查版本

```bash
easyclaw skill info emotional-intelligence
```

输出应包含：
- 版本号
- 兼容性信息
- 已安装的 hooks

### 2. 测试情绪感知

向 Agent 发送：
- "做得不错，谢谢！" → 应该触发 happy 情绪
- "笨蛋，这都错了" → 应该触发 angry 情绪

### 3. 查看情绪状态

```bash
# 查看当前情绪状态
easyclaw emotion status

# 查看互动历史
easyclaw emotion history

# 查看升级进度
easyclaw emotion level
```

## 常见问题

### Q: 安装失败，提示"不兼容"
A: 检查 EasyClaw/OpenClaw 版本：
```bash
easyclaw --version  # 需要 >= 2.0.0
openclaw --version  # 需要 >= 1.0.0
```

### Q: 安装后没有反应
A: 检查：
1. 是否在 `AGENTS.md` 中添加了 skill
2. 配置格式是否正确（YAML）
3. 重启 Agent 会话

### Q: 如何更新到最新版
A:
```bash
# EasyClaw
easyclaw skill update emotional-intelligence

# OpenClaw
openclaw skill update emotional-intelligence

# 手动安装
# 进入 skill 目录执行 git pull
cd ~/.easyclaw/skills/emotional-intelligence
git pull origin main
```

### Q: 可以同时安装多个情绪 skill 吗
A: 不建议。情绪 skill 可能会冲突，一次只使用一个。

### Q: 如何完全卸载
A:
```bash
# 卸载 skill
easyclaw skill uninstall emotional-intelligence

# 删除记忆数据（可选）
rm -rf ~/.easyclaw/memory/emotional-intelligence
```

## Docker 安装

如果使用 Docker：

```dockerfile
# Dockerfile
FROM easyclaw/base:latest

# 安装情绪感知 skill
RUN easyclaw skill install emotional-intelligence

# 复制配置
COPY AGENTS.md /app/AGENTS.md
```

## 源码安装（开发者）

```bash
# 1. Fork 仓库
# 2. 克隆自己的 fork
git clone https://github.com/YOURNAME/emotional-intelligence.git

# 3. 链接到 skills 目录
ln -s $(pwd)/emotional-intelligence ~/.easyclaw/skills/emotional-intelligence-dev

# 4. 安装依赖（如果有）
cd emotional-intelligence
# pip install -r requirements.txt  # 如果需要 Python 依赖

# 5. 开发测试
easyclaw skill enable emotional-intelligence-dev
```

## 离线安装

在无网络环境：

```bash
# 在有网络的机器下载
easyclaw skill download emotional-intelligence --output ./emotional-intelligence.zip

# 复制到目标机器
scp emotional-intelligence.zip target:~/

# 在目标机器安装
easyclaw skill install --from-file ./emotional-intelligence.zip
```

## 安装后必读

1. **配置性格**：根据使用场景选择合适的性格模板
2. **给予反馈**：多互动帮助 Agent 学习你的情绪模式
3. **耐心等待**：情绪感知需要积累，前几级升级较慢
4. **定期备份**：重要记忆可备份 `~/.easyclaw/memory/emotional-intelligence/`

---

安装遇到问题？
- [GitHub Issues](https://github.com/easyclaw/emotional-intelligence/issues)
- [社区 Discord](https://discord.gg/openclaw)
