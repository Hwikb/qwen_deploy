import requests

url = "http://127.0.0.1:8000//chat"
data = {"prompt": "你好，请介绍一下你自己。"}

resp = requests.post(url, json=data)
print(resp.json())
