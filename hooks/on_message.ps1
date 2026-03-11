# Emotional Intelligence Hook: on_message
# 在每次用户消息时触发情绪分析

param(
    [Parameter(Mandatory=$true)]
    [hashtable]$Context,
    
    [Parameter(Mandatory=$true)]
    [hashtable]$Config
)

# 加载情绪引擎
$enginePath = Join-Path $PSScriptRoot ".." "core" "emotion-engine.ps1"
. $enginePath

# 获取用户消息
$message = $Context.message
$userId = $Context.user_id
$sessionId = $Context.session_id

# 初始化或加载情绪状态
$emotionState = Get-EmotionState -UserId $userId

# 分析消息情绪
$detectedEmotion = Analyze-MessageEmotion `
    -Message $message `
    -Sensitivity ($Config.sensitivity ?? 3) `
    -CustomTriggers ($Config.custom_triggers ?? @{})

# 更新情绪状态
$emotionState = Update-EmotionState `
    -CurrentState $emotionState `
    -DetectedEmotion $detectedEmotion `
    -Context $Context

# 检查是否升级
$levelUp = Check-LevelUp -EmotionState $emotionState
if ($levelUp) {
    $emotionState.level = $levelUp.newLevel
    $emotionState.xp = $levelUp.remainingXP
    
    # 记录升级事件
    Write-Host "[Emotional Intelligence] Level Up! Now Lv.$($levelUp.newLevel)" -ForegroundColor Green
}

# 保存状态
Save-EmotionState -UserId $userId -State $emotionState

# 返回增强的上下文
$Context.emotion = @{
    state = $emotionState.currentState
    mood = $emotionState.mood
    intimacy = $emotionState.intimacy
    level = $emotionState.level
    shouldUseFormal = ($emotionState.mood -lt -3) -or ($emotionState.angryStreak -ge 2)
}

return $Context
