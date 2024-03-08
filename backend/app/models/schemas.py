# /app/models/schemas.py
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException


class ImageRequest(BaseModel):
    description: str

class ImageResponse(BaseModel):
    url: str
    description: str
