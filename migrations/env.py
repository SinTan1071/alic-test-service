# alembic/env.py
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- 新增：将项目 src 目录添加到 Python 路径 ---
# 这使得 Alembic 可以找到 src 下的模块
# .. 代表 alembic 目录的上一级，即项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)
# --- 新增结束 ---

# --- 修改：导入您的 Base 和配置加载函数 ---
from core.conf.conf import get_db_url # 从您的 conf.py 导入
from core.table.models import Base     # 从您的 models.py 导入
# --- 修改结束 ---

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata # <--- 保持这个设置

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # --- 修改：使用 get_db_url 获取 URL ---
    # url = config.get_main_option("sqlalchemy.url") # 不再从 ini 文件读取
    url = get_db_url() # 使用您的函数获取 URL
    # --- 修改结束 ---
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # --- 修改：使用 get_db_url 获取 URL 并设置 ---
    db_url = get_db_url()
    print(f"Using database URL from conf.py: {db_url[:db_url.find('://')+3]}...{db_url[db_url.rfind('@'):]}") # 打印部分 URL 用于确认，隐藏密码部分
    config.set_main_option('sqlalchemy.url', db_url)
    # --- 修改结束 ---

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        # --- 新增：确保 URL 被正确传递 ---
        # url=db_url # 如果 engine_from_config 不能正确获取，可以显式传递
        # --- 新增结束 ---
    )

    with connectable.connect() as connection:
        # --- 新增：打印确认连接信息 ---
        print(f"Successfully connected to database: {connection.engine.url.database}")
        # --- 新增结束 ---
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# --- 修改：根据 context.is_offline_mode() 调用不同的函数 ---
if context.is_offline_mode():
    print("Running migrations in offline mode...")
    run_migrations_offline()
else:
    print("Running migrations in online mode...")
    run_migrations_online()
# --- 修改结束 ---