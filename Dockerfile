FROM python:3.10-slim

# Metadata labels/tags
LABEL maintainer="AI-Empower-HQ-360 <contact@ai-empower-hq.com>"
LABEL version="0.1.0"
LABEL description="AI Film Studio - AI-powered film production API"
LABEL org.opencontainers.image.title="AI Film Studio API"
LABEL org.opencontainers.image.description="Production-ready container for AI Film Studio backend API"
LABEL org.opencontainers.image.version="0.1.0"
LABEL org.opencontainers.image.authors="AI-Empower-HQ-360"
LABEL org.opencontainers.image.url="https://github.com/AI-Empower-HQ-360/AI-Film-Studio"
LABEL org.opencontainers.image.source="https://github.com/AI-Empower-HQ-360/AI-Film-Studio"
LABEL org.opencontainers.image.vendor="AI-Empower-HQ-360"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "src.api.main"]
