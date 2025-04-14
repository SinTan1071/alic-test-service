from fastapi import FastAPI
from core.api.routes import router
from core.table.models import Base
from core.conf.conf import get_db_url
import uvicorn
from sqlalchemy import create_engine

app = FastAPI()
app.include_router(router, prefix="/api/v1")

# 初始化数据库表
engine = create_engine(get_db_url())
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)