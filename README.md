我们的绘画生成平台是一个创新性的基于自然语言的图像生成系统，可以理解您的文字描述并生成相应的图像，为您提供一个富有创意和互动的体验。它能够应对各种复杂的输入，如文学想象、艺术创作等，将这些文字转化为生动的图像。本系统是您随时待命的创意伙伴，能够激发您的创造力和想象力，帮助您将文字思维转化为视觉图像，让学习和创作过程更加生动有趣。

python版本为3.10.13。部分库要求写在requirements.txt中了。

前端在frontend文件夹下npm run serve，后端在backend文件夹下uvicorn app.main:app --host 0.0.0.0 --reload即可启动。

/backend/app/下的glm4.py和translator.py中分别需要[智谱清言api](https://maas.aminer.cn/)的key和[百度翻译api](https://api.fanyi.baidu.com/)的id和key（均有免费额度）。
