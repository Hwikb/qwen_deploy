# 🧠 Qwen-1.5-8B 本地部署与 API/Gradio 对话系统
本项目展示了如何在 Windows 本地环境 下部署 Qwen-1.5-8B
 大语言模型，
并通过 FastAPI 提供接口调用，以及使用 Gradio 构建网页对话界面。

## ⚙️ 环境配置
- 创建虚拟环境
```bash
conda create -n qwen python=3.10
conda activate qwen
```
- 安装依赖
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

## ⚙️ 模型下载
模型托管于 Hugging Face：
```bash
git lfs install
git clone https://huggingface.co/Qwen/Qwen-1.5-8B
```
⚠️ 注意：第一次克隆时需要使用 Hugging Face Token 登录

## 🚀 运行 FastAPI 服务
启动命令
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
运行example.py测试文件，可得到以下结果:
```bash
{'response': '你好，请介绍一下你自己。 作为一个AI模型，我没有实体形态，也无法感受情感或经历生活。我存在于互联网上，通过大量的数据和编程来理解人类语言和信息，并生成响应或回答问题。我可以处理大量文本、语音和图像输入，提供准确的翻译、摘要、写作建议、智能家居控制等服务。\n\n我的开发团队致力于构建智能助手、聊天机器人和其他自动化应用程序，以提高人们的生活质量和效率。例如，我可以作为在线客服代表，帮助用户解决常见问题；作为知识图谱搜索引擎，提供精准的信息搜索结果；作为语音识别系统，实现人机对话和自然语言处理；甚至作为机器翻译工具，将文本从一种语言翻译成另一种语言。\n\n我的功能和技术不断发展和完善，旨在更好地理解和满足用户需求，为用户提供更好的智能化体验。无论是科技爱好者还是日常使用者，我都希望成为你的朋友和帮手，提供有价值的帮助和支持。请随时告诉我你对某个话题的需求或问题，我会尽力为你提供相关信息和解答。'}
```

## 💬 启动 Gradio 本地网页
运行web_demo.py文件，可以在浏览器中访问以下网址：
```bash
http://127.0.0.1:7860
```
即可看到一个简洁的本地对话界面（类似 ChatGPT，支持连续对话）。
