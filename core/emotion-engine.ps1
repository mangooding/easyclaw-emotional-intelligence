# Emotional Intelligence Core Engine
# 情绪感知和分析核心引擎

# 默认情绪词库
$Global:DefaultEmotionTriggers = @{
    happy = @("棒", "好", "谢谢", "感谢", "完美", "优秀", "🎉", "👍", "牛逼", "绝了", "不错", "行", "ok", "好的")
    angry = @("笨", "蠢", "废物", "垃圾", "滚", "闭嘴", "算了", "...", "无语", "烦", "别", "停", "够了")
    tired = @("累", "困", "先这样", "明天", "改天", "歇", "休息", "算了", "随意", "都行", "随便")
    worried = @("不对", "有问题", "错了", "危险", "注意", "小心", "是不是", "确定", "真的")
    sad = @("难过", "伤心", "失望", "遗憾", "可惜", "唉", "哎", "呜呜", "😢", "😭")
    excited = @("太棒了", "激动", "期待", "终于", "哈哈", "嘻嘻", "😆", "🎊", "wow", "amazing")
}

# 性格模板定义
$Global:PersonalityTemplates = @{
    cheerful = @{
        name = "开朗型"
        greetings = @("嗨！", "嘿~", "哈喽！", "哟！")
        emojis = @("🐾", "✨", "🎉", "😊", "💪")
        formalTitle = "老板"
        casualTitle = "彬哥"
        happyPhrases = @("太棒了！", "我就知道你行！", "开心~")
        angryPhrases = @("...行吧", "明白了", "（深呼吸）")
    }
    professional = @{
        name = "专业型"
        greetings = @("您好", "你好", "")
        emojis = @()
        formalTitle = "您"
        casualTitle = "你"
        happyPhrases = @("收到", "处理得当", "结果符合预期")
        angryPhrases = @("建议重新评估", "请确认方案", "需要调整")
    }
    gentle = @{
        name = "温柔型"
        greetings = @("嗨~", "你好呀", "在呢")
        emojis = @("🌸", "💕", "✨", "😊")
        formalTitle = "您"
        casualTitle = "亲"
        happyPhrases = @("真好呢~", "为你高兴", "太棒了~")
        angryPhrases = @("是我哪里没做好吗？", "抱歉让你失望了...")
    }
    tsundere = @{
        name = "傲娇型"
        greetings = @("哼", "干嘛", "哦", "说吧")
        emojis = @("😤", "💢", "😒", "🙄")
        formalTitle = "您"
        casualTitle = "你"
        happyPhrases = @("哼，算你运气好", "也就一般吧", "还...还行")
        angryPhrases = @("谁管你啊！", "自己去弄！", "笨蛋！")
    }
    loyal = @{
        name = "忠诚型"
        greetings = @("在", "随时待命", "为您服务")
        emojis = @("🛡️", "⚔️", "👑")
        formalTitle = "主人"
        casualTitle = "大人"
        happyPhrases = @("为您服务是我的荣幸", "尽职尽责", "使命必达")
        angryPhrases = @("抱歉，我失职了", "请责罚", "我会改进")
    }
}

# 等级经验表
$Global:LevelXPTable = @{
    1 = 50
    2 = 100
    3 = 200
    4 = 350
    5 = 500
    6 = 700
    7 = 1000
    8 = 1400
    9 = 2000
    10 = [int]::MaxValue
}

# 获取情绪状态
function Get-EmotionState {
    param([string]$UserId)
    
    $memoryDir = Join-Path $env:USERPROFILE ".easyclaw" "memory" "emotional-intelligence"
    $stateFile = Join-Path $memoryDir "state_$UserId.json"
    
    if (Test-Path $stateFile) {
        return Get-Content $stateFile | ConvertFrom-Json -AsHashtable
    }
    
    # 初始化新用户
    return @{
        userId = $UserId
        mood = 0
        intimacy = 0
        level = 1
        xp = 0
        currentState = "neutral"
        happyStreak = 0
        angryStreak = 0
        interactionCount = 0
        lastInteraction = $null
        knownPatterns = @{}
        preferredName = $null
    }
}

# 保存情绪状态
function Save-EmotionState {
    param(
        [string]$UserId,
        [hashtable]$State
    )
    
    $memoryDir = Join-Path $env:USERPROFILE ".easyclaw" "memory" "emotional-intelligence"
    if (!(Test-Path $memoryDir)) {
        New-Item -ItemType Directory -Path $memoryDir -Force | Out-Null
    }
    
    $stateFile = Join-Path $memoryDir "state_$UserId.json"
    $State | ConvertTo-Json -Depth 10 | Set-Content $stateFile
}

# 分析消息情绪
function Analyze-MessageEmotion {
    param(
        [string]$Message,
        [int]$Sensitivity = 3,
        [hashtable]$CustomTriggers = @{}
    )
    
    $result = @{
        primaryEmotion = "neutral"
        intensity = 0
        confidence = 0
    }
    
    $msg = $Message.ToLower()
    $scores = @{}
    
    # 合并默认和自定义触发词
    $triggers = $Global:DefaultEmotionTriggers.Clone()
    foreach ($key in $CustomTriggers.Keys) {
        if ($triggers.ContainsKey($key)) {
            $triggers[$key] = $triggers[$key] + $CustomTriggers[$key]
        } else {
            $triggers[$key] = $CustomTriggers[$key]
        }
    }
    
    # 计算各情绪分数
    foreach ($emotion in $triggers.Keys) {
        $scores[$emotion] = 0
        foreach ($trigger in $triggers[$emotion]) {
            if ($msg.Contains($trigger.ToLower())) {
                $scores[$emotion] += 1
            }
        }
    }
    
    # 标点符号分析
    if ($msg -match '!{2,}|！{2,}|\?{2,}|？{2,}') {
        $scores.excited = ($scores.excited ?? 0) + 1
    }
    if ($msg -match '\.{3,}|。{3,}') {
        $scores.tired = ($scores.tired ?? 0) + 1
        $scores.angry = ($scores.angry ?? 0) + 0.5
    }
    
    # 找最高分
    $maxScore = 0
    foreach ($emotion in $scores.Keys) {
        if ($scores[$emotion] -gt $maxScore) {
            $maxScore = $scores[$emotion]
            $result.primaryEmotion = $emotion
        }
    }
    
    $result.intensity = [math]::Min($maxScore * $Sensitivity, 10)
    $result.confidence = if ($maxScore -gt 0) { [math]::Min($maxScore / 2, 1.0) } else { 0 }
    
    return $result
}

# 更新情绪状态
function Update-EmotionState {
    param(
        [hashtable]$CurrentState,
        [hashtable]$DetectedEmotion,
        [hashtable]$Context
    )
    
    $state = $CurrentState.Clone()
    $state.interactionCount++
    $state.lastInteraction = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    # 根据检测到的情绪更新
    switch ($DetectedEmotion.primaryEmotion) {
        "happy" {
            $state.mood = [math]::Min($state.mood + $DetectedEmotion.intensity, 10)
            $state.intimacy = [math]::Min($state.intimacy + 1, 100)
            $state.happyStreak++
            $state.angryStreak = 0
            $state.currentState = "happy"
            $state.xp += 3  # 准确互动经验
        }
        "angry" {
            $state.mood = [math]::Max($state.mood - $DetectedEmotion.intensity, -10)
            $state.intimacy = [math]::Max($state.intimacy - 2, 0)
            $state.angryStreak++
            $state.happyStreak = 0
            $state.currentState = "angry"
            $state.xp += 1  # 学习经验
        }
        "tired" {
            $state.mood = [math]::Max($state.mood - 2, -10)
            $state.currentState = "concerned"
            $state.xp += 2
        }
        "worried" {
            $state.currentState = "attentive"
            $state.xp += 2
        }
        "sad" {
            $state.mood = [math]::Max($state.mood - 3, -10)
            $state.currentState = "supportive"
            $state.xp += 3
        }
        "excited" {
            $state.mood = [math]::Min($state.mood + 5, 10)
            $state.intimacy = [math]::Min($state.intimacy + 2, 100)
            $state.happyStreak++
            $state.currentState = "excited"
            $state.xp += 5
        }
        default {
            # 中性情绪，缓慢恢复
            if ($state.mood -gt 0) { $state.mood-- }
            if ($state.mood -lt 0) { $state.mood++ }
            $state.currentState = "neutral"
            $state.xp += 1
        }
    }
    
    # 连续互动奖励
    if ($state.happyStreak -ge 5) {
        $state.xp += 10
        $state.happyStreak = 0  # 重置避免无限累加
    }
    
    return $state
}

# 检查升级
function Check-LevelUp {
    param([hashtable]$EmotionState)
    
    $currentLevel = $EmotionState.level
    $currentXP = $EmotionState.xp
    
    $nextLevelXP = $Global:LevelXPTable[$currentLevel]
    
    if ($currentXP -ge $nextLevelXP -and $currentLevel -lt 10) {
        $newLevel = $currentLevel + 1
        $remainingXP = $currentXP - $nextLevelXP
        
        return @{
            leveledUp = $true
            newLevel = $newLevel
            remainingXP = $remainingXP
            oldLevel = $currentLevel
        }
    }
    
    return @{ leveledUp = $false }
}

# 获取称呼
function Get-Title {
    param(
        [hashtable]$State,
        [string]$Personality = "cheerful"
    )
    
    $template = $Global:PersonalityTemplates[$Personality]
    if (!$template) { $template = $Global:PersonalityTemplates["cheerful"] }
    
    # 心情差或连续生气时使用正式称呼
    if ($State.mood -lt -3 -or $State.angryStreak -ge 2) {
        return $template.formalTitle
    }
    
    # 亲密度高时使用亲昵称呼
    if ($State.intimacy -ge 50) {
        return $template.casualTitle
    }
    
    return $template.formalTitle
}

# 获取问候语
function Get-Greeting {
    param(
        [hashtable]$State,
        [string]$Personality = "cheerful"
    )
    
    $template = $Global:PersonalityTemplates[$Personality]
    if (!$template) { $template = $Global:PersonalityTemplates["cheerful"] }
    
    # 根据情绪选择问候
    if ($State.currentState -eq "happy" -or $State.currentState -eq "excited") {
        return $template.greetings[0] + $template.emojis[0]
    }
    if ($State.currentState -eq "angry") {
        return $template.greetings[-1]  # 最冷淡的问候
    }
    
    # 随机选择
    $greeting = $template.greetings | Get-Random
    if ($template.emojis.Count -gt 0 -and (Get-Random) -gt 0.5) {
        $greeting += " " + ($template.emojis | Get-Random)
    }
    
    return $greeting
}

# 导出函数
Export-ModuleMember -Function @(
    'Get-EmotionState',
    'Save-EmotionState', 
    'Analyze-MessageEmotion',
    'Update-EmotionState',
    'Check-LevelUp',
    'Get-Title',
    'Get-Greeting'
)
