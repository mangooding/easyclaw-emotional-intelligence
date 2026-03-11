# 贡献指南

感谢你对 Emotional Intelligence Skill 的兴趣！我们欢迎各种形式的贡献。

## 如何贡献

### 报告 Bug

1. 先搜索 [Issues](https://github.com/easyclaw/emotional-intelligence/issues) 看是否已存在
2. 如果不存在，创建新 Issue，包含：
   - 问题描述
   - 复现步骤
   - 期望行为 vs 实际行为
   - 环境信息（OS, EasyClaw版本等）

### 提交功能请求

1. 描述你想解决的问题
2. 描述你想要的解决方案
3. 描述你考虑过的替代方案

### 提交代码

1. **Fork** 仓库
2. **Clone** 你的 fork
   ```bash
   git clone https://github.com/YOURNAME/emotional-intelligence.git
   ```
3. **创建分支**
   ```bash
   git checkout -b feature/my-new-feature
   # 或
   git checkout -b fix/bug-description
   ```
4. **编写代码**
   - 遵循现有代码风格
   - 添加必要的注释
   - 更新相关文档

5. **测试**
   ```bash
   # 运行测试
   powershell -File ./tests/run-tests.ps1
   ```

6. **提交**
   ```bash
   git add .
   git commit -m "feat: 添加新功能"
   # 或
   git commit -m "fix: 修复某个bug"
   ```

7. **Push 并创建 PR**
   ```bash
   git push origin feature/my-new-feature
   ```
   然后在 GitHub 创建 Pull Request

## 代码规范

### PowerShell 规范

```powershell
# ✅ 好的：使用完整参数名
Get-Content -Path $file

# ❌ 差的：使用缩写
cat $file

# ✅ 好的：有意义的变量名
$emotionState = Get-EmotionState

# ❌ 差的：模糊的名字
$es = Get-EmotionState

# ✅ 好的：添加注释
# 分析消息中的情绪关键词
$scores = Analyze-Keywords $message

# ✅ 好的：错误处理
try {
    $state = Get-EmotionState -UserId $userId
} catch {
    Write-Error "Failed to load emotion state: $_"
    return $null
}
```

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具相关

示例：
```
feat: 添加傲娇性格模板

- 实现 tsundere personality
- 添加专属问候语和emoji
- 更新文档
```

## 开发环境设置

```bash
# 1. 克隆仓库
git clone https://github.com/easyclaw/emotional-intelligence.git
cd emotional-intelligence

# 2. 链接到 EasyClaw skills 目录
# Windows (PowerShell)
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.easyclaw\skills\emotional-intelligence-dev" -Target (Get-Location).Path

# macOS/Linux
ln -s $(pwd) ~/.easyclaw/skills/emotional-intelligence-dev

# 3. 在测试 Agent 中启用开发版本
# 编辑 AGENTS.md，使用 emotional-intelligence-dev

# 4. 开发时实时监控
# 修改代码后，重启 Agent 会话即可测试
```

## 测试

### 运行测试

```bash
cd tests
powershell -File run-tests.ps1
```

### 手动测试清单

- [ ] 安装后技能正常加载
- [ ]  happy 情绪被正确识别
- [ ]  angry 情绪被正确识别
- [ ] 情绪状态持久化保存
- [ ] 升级系统正常工作
- [ ] 各性格模板切换正常
- [ ] 自定义触发词生效

## 添加新性格模板

想添加新性格？参考以下步骤：

1. 在 `core/emotion-engine.ps1` 的 `$Global:PersonalityTemplates` 中添加：

```powershell
mycustom = @{
    name = "自定义型"
    greetings = @("嗨", "你好", "哟")
    emojis = @("🎨", "✨")
    formalTitle = "您"
    casualTitle = "朋友"
    happyPhrases = @("太棒了！", "开心~")
    angryPhrases = @("呃...", "行吧")
}
```

2. 在 `hooks/on_response.ps1` 的 `$templates` 中添加对应的语气调整

3. 更新文档 `docs/personalities.md`

4. 提交 PR

## 添加新语言支持

想让情绪感知支持其他语言？

1. 在 `core/emotion-engine.ps1` 添加语言特定的触发词
2. 在配置中添加 `language` 选项
3. 更新 `Analyze-MessageEmotion` 函数支持多语言

## 文档贡献

- 发现文档错误？直接提 PR 修复
- 想添加教程？在 `docs/` 目录创建新文件
- 翻译文档？创建 `docs/zh/`, `docs/en/` 等子目录

## 社区行为准则

- 友善对待其他贡献者
- 尊重不同观点
- 接受建设性批评
- 关注社区利益

## 提问

- [GitHub Discussions](https://github.com/easyclaw/emotional-intelligence/discussions) - 一般讨论
- [Discord](https://discord.gg/openclaw) - 实时聊天

## 许可证

贡献即表示你同意你的代码使用 MIT 许可证。

---

再次感谢你的贡献！🦞
