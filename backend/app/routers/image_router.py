# /app/routers/image_router.py
import os
import uuid
import torch
from torch import autocast
from fastapi import Depends, APIRouter, HTTPException, Body
from ..schema.schemas import ImageRequest, ImageResponse, SelectImageRequest
from diffusers import StableDiffusionPipeline
from PIL import Image
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, Base
from database.models import Prompt, Image
from ..translator import translate
from ..glm4 import extend_description

os.environ["CUDA_VISIBLE_DEVICES"] = "1"
torch.backends.cudnn.benchmark = True

router = APIRouter()

GENERATED_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "generated")

local_model_path_v1 = (
    "/data/huggingface/hub/models--runwayml--stable-diffusion-v1-5/snapshots/1d0c4ebf6ff58a5caecab40fa1406526bca4b5b9")

# 加载模型
pipe = StableDiffusionPipeline.from_pretrained(
    local_model_path_v1,
    revision="fp16",
    torch_dtype=torch.float16
)
pipe.to("cuda")

lora_weights_path = "/data/picgen/caise.safetensors"
pipe.load_lora_weights(lora_weights_path)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_image_to_db(db: Session, file_path: str, text: str, translated_text: str, r_prompt: str):
    new_prompt = Prompt(text=text, translated_text=translated_text, real_prompt=r_prompt)
    db.add(new_prompt)
    db.commit()
    db.refresh(new_prompt)

    new_image = Image(file_path=file_path, prompt_id=new_prompt.id, creation_time=datetime.now())
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return new_image


def save_image(image, _prompt):
    os.makedirs(GENERATED_DIR, exist_ok=True)
    prompt_slug = _prompt.replace(" ", "_")[:12]
    filename = f"{prompt_slug}_{str(uuid.uuid4())[:8]}.png"
    image_path = os.path.join(GENERATED_DIR, filename)
    image.save(image_path)
    return filename


@router.post("/generate-image/", response_model=ImageResponse)
async def generate_image(request: ImageRequest, db: Session = Depends(get_db)):
    description = request.description
    print(f"Received description: {description}")
    images_info = []  # 用于保存图片信息的列表

    # 先扩写古诗
    description = extend_description(description)
    print(f"Extended description: {description}")

    translated_description = translate(description)
    print(f"Translated description: {translated_description}")

    prompt = f"{translated_description}, Chinese landscape, masterpiece, high details, best quality, 4k,"
    print(f"Prompt for image generation: {prompt}")

    with autocast("cuda"):
        for _ in range(2):
            image = pipe(
                width=768, height=432,
                prompt=prompt,
                negative_prompt="worst quality, low quality, watermark, calligraphy",
                # guidance_scale=0.7,
            ).images[0]
            filename = save_image(image, translated_description)
            file_path = os.path.join(GENERATED_DIR, filename)
            image_record = save_image_to_db(db, file_path, description, translated_description, prompt)

            image_url = f"http://10.177.58.143:8000/static/generated/{filename}"
            images_info.append({
                "id": image_record.id,  # 从数据库记录中获取图片ID
                "url": image_url  # 构建图片URL
            })

    return ImageResponse(images=images_info, description=request.description)  # 修改响应结构以包含图片ID和URL


# @router.post("/generate-image/", response_model=ImageResponse)
# async def generate_image(request: ImageRequest, db: Session = Depends(get_db)):
#     description = request.description
#     print(f"Received description: {description}")
#     images = []
#     filenames = []
#     # 翻译描述到英文
#     translated_description = translate(description)
#     print(f"Translated description: {translated_description}")
#
#     with autocast("cuda"):
#         for _ in range(2):
#             image = pipe(description).images[0]
#             filename = save_image(image, translated_description)
#             images.append(image)
#             filenames.append(filename)
#
#             file_path = os.path.join(GENERATED_DIR, filename)
#             save_image_to_db(db, file_path, description, translated_description, translated_description)
#
#     image_urls = [f"http://10.177.58.143:8000/static/generated/{filename}" for filename in filenames]
#     return ImageResponse(urls=image_urls, description=request.description)


@router.post("/select-image/")
async def select_image(request: SelectImageRequest, db: Session = Depends(get_db)):
    # 在数据库中查找对应的图片记录
    print(f'Select.image_id = {request.image_id}')
    img_to_update = db.query(Image).filter(Image.id == request.image_id).first()
    print(f'img_to_update = {img_to_update}')
    if not img_to_update:
        raise HTTPException(status_code=404, detail="Image not found")
    # 更新selected字段为True
    img_to_update.selected = True
    db.commit()
    return {"message": "Image selected successfully"}
