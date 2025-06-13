# 使用官方 Python 基础镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（包含 nmap 和 SSH 客户端）
RUN apt-get update && \
    apt-get install -y \
    nmap \
    telnet \
    openssh-client && \
    rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY ./src/backend/requirements.txt .
COPY ./src/backend /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install asyncssh telnetlib3 aiofiles

# 创建配置备份目录
RUN mkdir -p /app/config_backups && \
    chmod 777 /app/config_backups

# 暴露 FastAPI 端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]