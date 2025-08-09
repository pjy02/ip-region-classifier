# 使用官方Python运行时作为基础镜像
FROM python:3.11-slim-bullseye

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY iptest.py .
COPY README.md .
COPY LICENSE .

# 创建数据目录
RUN mkdir -p /app/data /app/output

# 创建非root用户
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# 暴露端口（如果需要的话）
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; print('Container is healthy')" || exit 1

# 默认命令
CMD ["python", "iptest.py", "--help"]

# 标签
LABEL maintainer="IP Region Classifier Team"
LABEL version="1.0.0"
LABEL description="A tool for classifying IP addresses by geographic region"