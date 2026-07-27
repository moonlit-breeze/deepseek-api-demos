"""
调用 DeepSeek API，问"什么是无我"，打印返回的 JSON 中 content 字段。
运行前需设置环境变量：DEEPSEEK_API_KEY=你的key
运行方式：python FoQaPython.py
"""

import os
import json
import urllib.request

API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not API_KEY:
    print("请先设置环境变量 DEEPSEEK_API_KEY")
    exit(1)

data = {
    "model": "deepseek-v4-flash",
    "messages": [
        {"role": "user", "content": "什么是无我"}
    ],
    "stream": False
}

req = urllib.request.Request(
    "https://api.deepseek.com/chat/completions",
    data=json.dumps(data).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    method="POST"
)

with urllib.request.urlopen(req, timeout=60) as resp:
    body = json.loads(resp.read().decode("utf-8"))

if "error" in body:
    print(f"API 返回错误：{body['error']['message']}")
    exit(1)

print(body["choices"][0]["message"]["content"])
