# Emotional Intelligence Skill - Docker Support
# Version: 2.1.1

FROM python:3.11-slim

LABEL maintainer="EasyClaw Community"
LABEL version="2.1.1"
LABEL description="Emotional Intelligence Skill for OpenClaw/EasyClaw Agents"

# 安装依赖
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --no-cache-dir \
    pyyaml \
    dataclasses \
    typing-extensions

# 设置工作目录
WORKDIR /app

# 创建必要的目录
RUN mkdir -p /app/skills /app/memory /app/config

# 复制技能文件
COPY . /app/skills/emotional-intelligence/

# 设置环境变量
ENV PYTHONPATH=/app/skills/emotional-intelligence:$PYTHONPATH
ENV EI_PLATFORM=docker
ENV EMOTIONAL_PERSONALITY=cheerful
ENV EMOTIONAL_SENSITIVITY=3
ENV EMOTIONAL_PERSISTENCE=true
ENV SUBCONSCIOUS_ENABLED=true
ENV DREAM_STATE_ENABLED=true

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "from adapters.openclaw_adapter import check_health; print(check_health())" || exit 1

# 默认命令
CMD ["python3", "-c", "print('Emotional Intelligence Skill v2.1.1 is ready')"]
