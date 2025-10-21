from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI()

# 加载模型
model_path = "./Qwen1.5-1.8B-Chat"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
).eval()

class Query(BaseModel):
    prompt: str

@app.post("/chat")
def chat(query: Query):
    inputs = tokenizer(query.prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=512)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": answer}
