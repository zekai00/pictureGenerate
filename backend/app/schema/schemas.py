# /app/models/schemas.py
from pydantic import BaseModel, HttpUrl
from typing import List
from fastapi import FastAPI, HTTPException


class SelectImageRequest(BaseModel):
    image_id: int


class ImageRequest(BaseModel):
    description: str


class ImageInfo(BaseModel):
    id: int
    url: str


class ImageResponse(BaseModel):
    images: List[ImageInfo]
    description: str
