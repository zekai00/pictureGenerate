# /app/routers/image_router.py
import os
import uuid
from fastapi import APIRouter, HTTPException
from models.schemas import ImageRequest, ImageResponse
from diffusers import StableDiffusionPipeline
from PIL import Image
from fastapi.responses import FileResponse


router = APIRouter()

GENERATED_DIR = os.path.join(os.path.dirname(__file__), "generated")

# 加载模型
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

def save_image(image):
    # 确保 generated 文件夹存在
    os.makedirs(GENERATED_DIR, exist_ok=True)

    # 生成唯一的文件名
    filename = f"{uuid.uuid4()}.png"
    image_path = os.path.join(GENERATED_DIR, filename)

    # 保存图像
    image.save(image_path)

    return filename

@router.post("/generate-image/", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    # 获取用户输入的描述
    description = request.description
    print(f"Received description: {description}")

    # 使用模型生成图像
    image = pipe(description).images[0]
    
    # 保存生成的图像并获取保存路径 (下一步会讨论保存路径)
    filename = save_image(image)

    # 示例URL，这里应替换为调用图像生成逻辑后的图像URL
    # image_url = "http://127.0.0.1:8000/static/pic1.png"
    image_url = f"http://127.0.0.1:8000/static/generated/{filename}"
    return ImageResponse(url=image_url, description=request.description)
