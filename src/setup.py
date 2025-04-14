from setuptools import setup, find_packages

setup(
    name="fastapi-service",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "sqlalchemy>=1.4.0",
        "psycopg2-binary>=2.9.0",
        "setuptools>=70.0.0",
        "pydantic>=1.8.0",
        "alembic>=1.7.0",
        "pyyaml>=6.0"  # 新增YAML依赖
    ],
)