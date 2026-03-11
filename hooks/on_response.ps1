# Emotional Intelligence Hook: on_response
# 在生成回复前调整语气和内容

param(
    [Parameter(Mandatory=$true)]
    [hashtable]$Context,
    
    [Parameter(Mandatory=$true)]
    [string]$Response,
    
    [Parameter(Mandatory=$true)]
    [hashtable]$Config
)

# 加载情绪引擎
$enginePath = Join-Path $PSScriptRoot ".." "core" "emotion-engine.ps1"
. $enginePath

$userId = $Context.user_id
$emotion = $Context.emotion
$personality = $Config.personality ?? "cheerful"

# 获取情绪状态
$state = Get-EmotionState -UserId $userId

# 加载性格模板
$templates = @{
    cheerful = @{
        toneModifiers = @{
            happy = @{ prefix = ""; suffix = " 🎉"; style = "energetic" }
            angry = @{ prefix = ""; suffix = ""; style = "distant" }
            concerned = @{ prefix = ""; suffix = " 还好吗？"; style = "gentle" }
            neutral = @{ prefix = ""; suffix = ""; style = "normal" }
        }
        useEmoji = $true
        useTitle = $true
    }
    professional = @{
        toneModifiers = @{
            happy = @{ prefix = "收到。"; suffix = ""; style = "acknowledging" }
            angry = @{ prefix = "明白。"; suffix = ""; style = "formal" }
            concerned = @{ prefix = "注意："; suffix = ""; style = "alert" }
            neutral = @{ prefix = ""; suffix = ""; style = "normal" }
        }
        useEmoji = $false
        useTitle = $false
    }
    gentle = @{
        toneModifiers = @{
            happy = @{ prefix = "真好呢~ "; suffix = " 💕"; style = "warm" }
            angry = @{ prefix = "抱歉..."; suffix = " 我会注意的"; style = "apologetic" }
            concerned = @{ prefix = ""; suffix = " 需要休息吗？"; style = "caring" }
            neutral = @{ prefix = ""; suffix = "~"; style = "soft" }
        }
        useEmoji = $true
        useTitle = $true
    }
    tsundere = @{
        toneModifiers = @{
            happy = @{ prefix = "哼，"; suffix = " 也就那样"; style = "tsun" }
            angry = @{ prefix = "笨蛋！"; suffix = " 自己去想！"; style = "mad" }
            concerned = @{ prefix = "喂，"; suffix = " 别死啊"; style = "dere" }
            neutral = @{ prefix = ""; suffix = " 快点说"; style = "casual" }
        }
        useEmoji = $true
        useTitle = $true
    }
    loyal = @{
        toneModifiers = @{
            happy = @{ prefix = "遵命。"; suffix = " 为您服务"; style = "loyal" }
            angry = @{ prefix = "属下知罪。"; suffix = ""; style = "submissive" }
            concerned = @{ prefix = "主上，"; suffix = " 请保重"; style = "caring" }
            neutral = @{ prefix = "在。"; suffix = ""; style = "ready" }
        }
        useEmoji = $false
        useTitle = $true
    }
}

$template = $templates[$personality]
if (!$template) { $template = $templates["cheerful"] }

# 获取当前情绪对应的语气调整
$currentState = $state.currentState
if (!$template.toneModifiers.ContainsKey($currentState)) {
    $currentState = "neutral"
}
$modifier = $template.toneModifiers[$currentState]

# 调整回复
$adjustedResponse = $Response

# 添加前缀（如果不是以该前缀开头）
if ($modifier.prefix -and !$adjustedResponse.StartsWith($modifier.prefix)) {
    # 检查是否已经有问候语
    $hasGreeting = $false
    foreach ($greeting in @("嗨", "嘿", "你好", "哈喽", "在", "您好", "遵命", "哼")) {
        if ($adjustedResponse.StartsWith($greeting)) {
            $hasGreeting = $true
            break
        }
    }
    
    if (!$hasGreeting -and $template.useTitle) {
        $title = Get-Title -State $state -Personality $personality
        if ($title -and !$adjustedResponse.Contains($title)) {
            $adjustedResponse = $title + "，" + $adjustedResponse
        }
    }
}

# 添加后缀
if ($modifier.suffix -and !$adjustedResponse.EndsWith($modifier.suffix.Trim())) {
    # 检查是否已经以标点结尾
    if ($adjustedResponse -match '[。！？.!?~]$') {
        # 替换最后的标点
        $adjustedResponse = $adjustedResponse -replace '[。！？.!?~]$', $modifier.suffix
    } else {
        $adjustedResponse += $modifier.suffix
    }
}

# 根据心情调整emoji使用
if ($template.useEmoji -and $personality -eq "cheerful") {
    $emojis = @("🐾", "✨", "🎉", "😊", "💪", "👍", "🌟")
    
    # 心情好，多加点emoji
    if ($state.mood -gt 5 -and (Get-Random) -gt 0.3) {
        $emoji = $emojis | Get-Random
        if (!$adjustedResponse.Contains($emoji)) {
            $adjustedResponse += " " + $emoji
        }
    }
    
    # 心情不好，减少emoji或不用
    if ($state.mood -lt -3) {
        # 移除所有emoji
        foreach ($emoji in $emojis) {
            $adjustedResponse = $adjustedResponse.Replace($emoji, "")
        }
        $adjustedResponse = $adjustedResponse.Trim()
    }
}

# 心情很差时，回复更简短冷淡
if ($state.mood -lt -5) {
    $sentences = $adjustedResponse -split '[。！？.!?]'
    if ($sentences.Count -gt 2) {
        $adjustedResponse = $sentences[0] + "。"
    }
}

# 亲密度高时，添加个性化内容
if ($state.intimacy -ge 70 -and $state.interactionCount -gt 50) {
    # 可以在这里添加更亲昵的表达
    $intimacyPhrases = @(
        "老规矩",
        "还是老样子",
        "懂你意思"
    )
    
    if ((Get-Random) -gt 0.7 -and $state.mood -gt 0) {
        $phrase = $intimacyPhrases | Get-Random
        if (!$adjustedResponse.Contains($phrase)) {
            $adjustedResponse = $adjustedResponse -replace '[。！？.!?~]$', "，$phrase$&"
        }
    }
}

return $adjustedResponse
