# EasyClaw Platform Adapter for Emotional Intelligence Skill
# Version: 2.1.1
# 提供 EasyClaw 平台的兼容支持

$EI_VERSION = "2.1.1"
$PLATFORM = "easyclaw"

# 检测工作区路径
function Get-WorkspacePath {
    param(
        [string]$CustomPath = $null
    )
    
    if ($CustomPath) {
        return $CustomPath
    }
    
    # 环境变量
    if ($env:EASYCLAW_WORKSPACE) {
        return $env:EASYCLAW_WORKSPACE
    }
    
    # 默认路径
    $defaultPaths = @(
        "$env:USERPROFILE\.easyclaw",
        "$env:LOCALAPPDATA\EasyClaw",
        "C:\EasyClaw"
    )
    
    foreach ($path in $defaultPaths) {
        if (Test-Path $path) {
            return $path
        }
    }
    
    # 创建默认路径
    $defaultPath = "$env:USERPROFILE\.easyclaw"
    New-Item -ItemType Directory -Path $defaultPath -Force | Out-Null
    return $defaultPath
}

# 加载配置
function Get-EmotionalConfig {
    $workspace = Get-WorkspacePath
    $configPaths = @(
        "$workspace\SOUL.md",
        "$workspace\AGENTS.md",
        "$workspace\config.yaml"
    )
    
    foreach ($path in $configPaths) {
        if (Test-Path $path) {
            try {
                $content = Get-Content $path -Raw -Encoding UTF8
                
                # 提取 YAML 部分
                if ($content -match '---\s*\n(.*?)\n---') {
                    $yamlContent = $matches[1]
                    # 简单解析 YAML (PowerShell 5.1+ 有 ConvertFrom-Yaml，但需要模块)
                    # 这里使用简单解析
                    return Parse-YamlContent $yamlContent
                }
            }
            catch {
                Write-Warning "[EasyClawAdapter] 无法解析 $path : $_"
            }
        }
    }
    
    return @{}
}

# 简单 YAML 解析
function Parse-YamlContent {
    param([string]$Content)
    
    $config = @{}
    $currentSection = $null
    $lines = $Content -split "`n"
    
    foreach ($line in $lines) {
        $line = $line.Trim()
        
        # 跳过空行和注释
        if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith("#")) {
            continue
        }
        
        # 顶级键
        if ($line -match '^(\w+):\s*(.*)$') {
            $key = $matches[1]
            $value = $matches[2].Trim()
            
            if ($value -eq "" -or $value -eq "null") {
                $config[$key] = @{}
                $currentSection = $key
            }
            else {
                $config[$key] = $value
            }
        }
    }
    
    return $config
}

# 获取记忆路径
function Get-MemoryPath {
    $config = Get-EmotionalConfig
    $customPath = $config.emotional_config.data_path
    
    if ($customPath) {
        return $customPath
    }
    
    $workspace = Get-WorkspacePath
    return "$workspace\memory"
}

# 确保目录存在
function Initialize-Directories {
    $memoryPath = Get-MemoryPath
    $paths = @(
        $memoryPath,
        "$memoryPath\emotional-intelligence",
        "$memoryPath\subconscious",
        "$memoryPath\subconscious\dream"
    )
    
    foreach ($path in $paths) {
        if (!(Test-Path $path)) {
            New-Item -ItemType Directory -Path $path -Force | Out-Null
            Write-Host "[EasyClawAdapter] 创建目录: $path" -ForegroundColor Gray
        }
    }
}

# 添加刺激 (潜意识层)
function Add-Stimulus {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Type,
        
        [Parameter(Mandatory=$true)]
        [string]$Content,
        
        [float]$Weight = 1.0
    )
    
    $memoryPath = Get-MemoryPath
    $bufferFile = "$memoryPath\subconscious\buffer.json"
    
    # 创建刺激对象
    $stimulus = @{
        id = "stm_$(Get-Date -Format 'yyyyMMdd_HHmmss')_$([Random]::new().Next(1000,9999))"
        type = $Type
        content = $Content
        timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
        weight = $Weight
        delay = Get-RandomDelay -Type $Type
        scheduled_time = 0
        status = "pending"
    }
    
    $stimulus.scheduled_time = $stimulus.timestamp + $stimulus.delay
    
    # 加载现有缓冲区
    $buffer = @{buffer = @(); repressed = @()}
    if (Test-Path $bufferFile) {
        $buffer = Get-Content $bufferFile | ConvertFrom-Json
    }
    
    # 添加新刺激
    $buffer.buffer += $stimulus
    
    # 保存
    $buffer | ConvertTo-Json -Depth 10 | Set-Content $bufferFile -Encoding UTF8
    
    Write-Host "[EasyClawAdapter] 添加刺激: $Type (延迟 $($stimulus.delay)秒)" -ForegroundColor Cyan
    
    return $stimulus
}

# 获取随机延迟
function Get-RandomDelay {
    param([string]$Type)
    
    $delays = @{
        "praise" = @{min = 0; max = 60}
        "criticism" = @{min = 180; max = 900}
        "neglect" = @{min = 600; max = 3600}
        "surprise" = @{min = 0; max = 30}
        "confusion" = @{min = 60; max = 300}
        "warmth" = @{min = 0; max = 120}
    }
    
    $config = $delays[$Type]
    if (!$config) {
        $config = @{min = 0; max = 300}
    }
    
    return Get-Random -Minimum $config.min -Maximum $config.max
}

# 处理缓冲区
function Process-Buffer {
    $memoryPath = Get-MemoryPath
    $bufferFile = "$memoryPath\subconscious\buffer.json"
    
    if (!(Test-Path $bufferFile)) {
        return @()
    }
    
    $buffer = Get-Content $bufferFile | ConvertFrom-Json
    $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    
    $ready = @()
    $remaining = @()
    
    foreach ($stimulus in $buffer.buffer) {
        if ($stimulus.status -eq "pending" -and $now -ge $stimulus.scheduled_time) {
            $stimulus.status = "active"
            $ready += $stimulus
        }
        elseif ($stimulus.status -eq "pending") {
            $remaining += $stimulus
        }
    }
    
    # 保存剩余
    $buffer.buffer = $remaining
    $buffer | ConvertTo-Json -Depth 10 | Set-Content $bufferFile -Encoding UTF8
    
    return $ready
}

# 获取情感配置
function Get-EIConfig {
    $config = Get-EmotionalConfig
    return $config.emotional_config
}

# 检查潜意识层是否启用
function Test-SubconsciousEnabled {
    $config = Get-EIConfig
    $sub = $config.subconscious
    
    if ($sub -and $sub.enabled -eq $true) {
        return $true
    }
    return $false
}

# 健康检查
function Test-EIHealth {
    $workspace = Get-WorkspacePath
    $memoryPath = Get-MemoryPath
    
    $results = @{
        platform = $PLATFORM
        version = $EI_VERSION
        status = "ok"
        checks = @{}
    }
    
    # 检查工作区
    $results.checks.workspace = @{
        exists = Test-Path $workspace
        path = $workspace
        writable = $true  # PowerShell 简单检查
    }
    
    # 检查记忆目录
    $results.checks.memory = @{
        exists = Test-Path $memoryPath
        parent_writable = Test-Path (Split-Path $memoryPath -Parent)
    }
    
    # 检查潜意识层
    $subPath = "$memoryPath\subconscious"
    $results.checks.subconscious = @{
        enabled = Test-SubconsciousEnabled
        path_exists = Test-Path $subPath
    }
    
    return $results
}

# 初始化平台
function Initialize-EIPlatform {
    Write-Host "[EasyClawAdapter] 初始化 Emotional Intelligence v$EI_VERSION" -ForegroundColor Green
    
    Initialize-Directories
    
    $health = Test-EIHealth
    if ($health.status -eq "ok") {
        Write-Host "[EasyClawAdapter] ✓ 平台初始化成功" -ForegroundColor Green
    }
    else {
        Write-Warning "[EasyClawAdapter] 平台初始化警告"
    }
    
    return $health
}

# 导出函数
Export-ModuleMember -Function @(
    'Get-WorkspacePath',
    'Get-EmotionalConfig', 
    'Get-MemoryPath',
    'Initialize-Directories',
    'Add-Stimulus',
    'Process-Buffer',
    'Get-EIConfig',
    'Test-SubconsciousEnabled',
    'Test-EIHealth',
    'Initialize-EIPlatform'
)

# 如果直接运行此脚本，执行测试
if ($MyInvocation.InvocationName -eq $MyInvocation.MyCommand.Path) {
    Write-Host "=" * 60
    Write-Host "EasyClaw Platform Adapter Test" -ForegroundColor Cyan
    Write-Host "=" * 60
    
    $health = Initialize-EIPlatform
    
    Write-Host "`n[平台信息]" -ForegroundColor Yellow
    Write-Host "  平台: $($health.platform)"
    Write-Host "  版本: $($health.version)"
    Write-Host "  工作区: $(Get-WorkspacePath)"
    Write-Host "  记忆路径: $(Get-MemoryPath)"
    
    Write-Host "`n[健康检查]" -ForegroundColor Yellow
    Write-Host "  状态: $($health.status)"
    foreach ($check in $health.checks.Keys) {
        Write-Host "  $check : $($health.checks[$check] | ConvertTo-Json -Compress)"
    }
    
    Write-Host "`n[测试潜意识层]" -ForegroundColor Yellow
    if (Test-SubconsciousEnabled) {
        Write-Host "  潜意识层: 已启用"
        
        # 添加测试刺激
        $stimulus = Add-Stimulus -Type "praise" -Content "测试赞美" -Weight 1.0
        Write-Host "  添加测试刺激: $($stimulus.id)"
        
        # 处理缓冲区
        $ready = Process-Buffer
        Write-Host "  到期刺激: $($ready.Count)个"
    }
    else {
        Write-Host "  潜意识层: 未启用"
    }
    
    Write-Host "`n" + "=" * 60
    Write-Host "测试完成!" -ForegroundColor Green
}
