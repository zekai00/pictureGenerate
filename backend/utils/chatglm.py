from transformers import AutoTokenizer, AutoModel
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0, 1"
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
model_path = ("/data/huggingface/hub/models--THUDM--chatglm3-6b-base/snapshots/f91a1de587fdc692073367198e65369669a0b49d/")

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(4).cuda()

model = model.eval()
response, history = model.chat(tokenizer, "你好", history=[])
print(response)
response, history = model.chat(tokenizer, "把白日依山尽扩写一下，我需要50个字。", history=history)
print(response)


# inputs = tokenizer([""], return_tensors="pt").to('cuda')
# outputs = model.generate(**inputs)
# print(tokenizer.decode(outputs[0].tolist()))
