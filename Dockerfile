# alic-test-db-service/Dockerfile

# 1. 选择一个 Python 基础镜像
# 使用 slim 版本可以减小镜像体积
FROM python:3.11-slim

# 2. 设置工作目录
# 容器内的所有后续操作都将在此目录下进行
WORKDIR /app

# 3. 复制依赖文件
# 先复制 requirements.txt，以便利用 Docker 的层缓存机制
# 只有当 requirements.txt 变化时，后续的 pip install 才会重新运行
COPY requirements.txt ./

# 4. 安装依赖
# 升级 pip 并安装 requirements.txt 中的所有包
# --no-cache-dir 选项可以减小镜像体积
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. 复制项目代码
# 将当前目录下的 app.py 和 src 目录复制到容器的 /app 目录下
COPY app.py .
COPY src ./src
# 构建完成后删除镜像中的配置文件

# 6. 暴露端口
# 声明容器将监听 8080 端口
EXPOSE 8080

# 7. 运行应用的命令
# 使用 uvicorn 启动 FastAPI 应用
# 注意：在生产环境中通常不使用 --reload 标志
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
