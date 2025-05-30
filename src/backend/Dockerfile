FROM python:3.13-slim

WORKDIR /app

# 1. 先复制依赖文件并安装
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 2. 复制项目代码（排除 .env 和缓存文件）
COPY . /app

# 3. 环境变量配置
ENV PYTHONPATH=/app \
    PORT=8000 \
    HOST=0.0.0.0

# 4. 安全设置
RUN find /app -name "*.pyc" -delete && \
    find /app -name "__pycache__" -exec rm -rf {} +

# 5. 启动命令（修正路径）
CMD ["uvicorn", "src.backend.app:app", "--host", "0.0.0.0", "--port", "8000"]