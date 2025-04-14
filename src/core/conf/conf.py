import os
# import yaml # 不再需要
# from pathlib import Path # 不再需要

# BASE_DIR = Path(__file__).resolve().parent.parent # 不再需要

# def load_config(): # 可以移除或重构
#     # ... 不再从文件加载 ...
#     pass

def get_db_url():
    # 从环境变量读取配置
    db_driver = os.environ.get('DB_DRIVER', 'postgresql+psycopg2') # 提供默认值
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD') # 重要：从环境变量获取密码
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT') # 提供默认值
    db_name = os.environ.get('DB_NAME')

    if not all([db_user, db_password, db_host, db_name]):
        raise ValueError("Missing one or more database connection environment variables (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)")

    # 确保驱动程序兼容性，例如 psycopg2 需要 postgresql+psycopg2
    # 如果你的 driver 环境变量就是 postgresql，可能需要调整
    # return f"{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    # 假设 DB_DRIVER 环境变量已经包含 driver+adapter, e.g., 'postgresql+psycopg2'
    return f"{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"