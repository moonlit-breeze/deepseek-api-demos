import os
import json
import urllib.request

API_URL = "https://api.deepseek.com/chat/completions"
API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not API_KEY:
    print("请先设置环境变量 DEEPSEEK_API_KEY")
    exit(1)

SYSTEM_PROMPT = """你是一位佛学教授，专门解答佛法问题。
请严格参照以下示例的格式回答。

示例1：
问：什么是五戒？
答：五戒是佛教在家弟子应持的根本戒律，包括不杀生、不偷盗、不邪淫、不妄语、不饮酒。
出处：《长阿含经》《增一阿含经》

示例2：
问：不偷盗戒的范围？
答：不偷盗戒禁止一切不与而取的行为，包括直接窃取、骗取、侵占，乃至借而不还。
出处：《四分律》卷一

请按照上述格式回答用户的新问题。"""


def ask(system, user, model="deepseek-v4-flash"):
    data = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        "temperature": 0.3
    }).encode()

    req = urllib.request.Request(API_URL, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    })

    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    if "error" in body:
        print(f"API 返回错误：{body['error']['message']}")
        exit(1)

    return body["choices"][0]["message"]["content"]


if __name__ == "__main__":
    question = "不饮酒戒的例外情况？"
    print("问题:", question)
    print()
    print("回答:")
    print(ask(SYSTEM_PROMPT, question))
