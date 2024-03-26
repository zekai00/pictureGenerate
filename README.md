本平台的主要功能为：用户可以输入一首古诗，得到两幅由古诗生成的图像。

python版本为3.10.13。部分库要求写在requirements.txt中了。

前端在frontend文件夹下npm run serve，后端在backend文件夹下uvicorn app.main:app --host 0.0.0.0 --reload即可启动。

/backend/app/下的glm4.py和translator.py中分别需要[智谱清言api](https://maas.aminer.cn/)的key和[百度翻译api](https://api.fanyi.baidu.com/)的id和key（均有免费额度）。
