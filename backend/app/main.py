# /app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers.image_router import router as image_router
from .translator import translate
from database import create_tables
import os
print(os.getcwd())
import sys
from pathlib import Path
# 获取 backend 目录的路径
backend_dir = Path(__file__).resolve().parent.parent
# 将 backend 目录的路径添加到 sys.path
if str(backend_dir) not in sys.path:
    sys.path.append(str(backend_dir))

app = FastAPI()

app.mount("/static", StaticFiles(directory="/data/picgen/backend/app/static"), name="static")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，出于安全考虑，应当更具体地指定允许的来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

app.include_router(image_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.on_event("startup")
def startup():
    create_tables()  # create tables if not exist


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()