# lifespan.py

from diffusers import StableDiffusionPipeline
import torch

class Lifespan:
    def __init__(self):
        self.model = None

    async def startup(self):
        self.model = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        if torch.cuda.is_available():  # 这里检查 CUDA 是否可用
            self.model.to("cuda")
        else:
            self.model.to("cpu")
        print("Model loaded and moved to device.")

    async def shutdown(self):
        print("Application shutdown.")
        # 清理代码（如果需要）可以放在这里

# 创建 Lifespan 实例
lifespan = Lifespan()
