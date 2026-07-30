import os, json, urllib.request

API_URL = "https://api.deepseek.com/chat/completions"
API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not API_KEY:
    print("请先设置环境变量 DEEPSEEK_API_KEY")
    exit(1)

system_prompt = """你是一位律师，负责分析法律问题。

请按以下步骤回答：
1. 先列出本案涉及的关键法律条文
2. 逐条分析是否适用于本案
3. 最后给出综合结论

格式要求：
【法律依据】
（逐条列出）
【分析】
（逐条分析）
【结论】
（一句话总结）"""

user_message = "张三在网上散布李四的隐私信息，是否构成侵权？"

# system_prompt = """你是一位佛法教授，负责解答佛法问题。

# 请按以下步骤回答：
# 1. 先回答涉及的关键佛法经论
# 2. 结合经论逐条分析其含义
# 3. 最后给出综合结论

# 格式要求：
# 【经论依据】
# （逐条列出）
# 【分析】
# （逐条分析）
# 【结论】
# （一句话总结）"""

# user_message = "烦恼即菩提是什么意思？"

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
    print(call_deepseek(system_prompt, user_message))
