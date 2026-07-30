import os, json, urllib.request

API_URL = "https://api.deepseek.com/chat/completions"
API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not API_KEY:
    print("请先设置环境变量 DEEPSEEK_API_KEY")
    exit(1)

system_prompt = """你是佛学知识库。请用 JSON 格式回答戒律相关问题。
JSON 必须包含以下字段：
- question: 用户的问题（字符串）
- answer: 完整回答（字符串）
- source: 经典出处（字符串，如不确定写"待查"）

仅返回 JSON，不要加任何解释文字。"""

user_message = "什么是菩萨戒？"

def call_deepseek(system_prompt, user_message):
    data = json.dumps({
        "model": "deepseek-v4-flash",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }).encode()
    req = urllib.request.Request(API_URL, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    })
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())

        if "error" in body:
            print(f"API 返回错误：{body['error']['message']}")
            exit(1)

    return body["choices"][0]["message"]["content"]

if __name__ == "__main__":
    answer = call_deepseek(system_prompt, user_message)
    print(answer)