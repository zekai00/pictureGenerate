# /app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers.image_router import router as image_router
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

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
