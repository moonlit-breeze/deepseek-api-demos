# Prompt 工程速查笔记（直接上手版）

> 面向 Python 初学者，不写废话。配合 DeepSeek API 使用。

---

## 一、搞懂一个公式

**好 Prompt = 角色 + 任务 + 格式 + 示例**

```
你是一个[角色]，请帮我[做什么]。按以下格式输出：[格式]。参考示例：[给 2-3 个例子]
```

把这四个要素补齐，你的 Prompt 就已经超过 80% 的人了。

---

## 二、三个必须掌握的技巧

### 1. Few-shot：给例子，不用解释

**一句话**：把你要的输出样式写成 2-3 个例子塞进 prompt，模型会照着学。

**反面教材（零样本，AI 爱放飞）**：

```
解释"不杀生戒"。
```

AI 可能输出 500 字论文。

**正确做法（给例子，AI 照着抄格式）**：

```python
system_prompt = """你是一位佛学教授，专门解答戒律问题。
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

user_message = "不饮酒戒的例外情况？"
```

**对应今天要写的脚本**：`prompt_few_shot.py`

---

### 2. Chain-of-Thought（CoT）：让 AI 先想再说

**一句话**：在 prompt 里加一句「请先分析，再给出结论」，模型准确率飙升。

**为什么有效**：不给思考空间，AI 相当于闭眼答题。让它先推理再输出，等于给了它草稿纸。

**写法**：

```python
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
```

**更简单粗暴的写法**（一句就够了）：

```
请一步步思考后再回答。
```

翻译成英文 `Let's think step by step.` 对某些模型效果更好。

**对应今天要写的脚本**：`prompt_cot.py`

---

### 3. 结构化输出：让 AI 吐 JSON

**一句话**：要求返回 JSON，方便你写代码解析。指定字段名和类型。

**写法**：

```python
system_prompt = """你是佛学知识库。请用 JSON 格式回答戒律相关问题。
JSON 必须包含以下字段：
- question: 用户的问题（字符串）
- answer: 完整回答（字符串）
- source: 经典出处（字符串，如不确定写"待查"）

仅返回 JSON，不要加任何解释文字。"""

user_message = "什么是菩萨戒？"
```

**期望输出**：

```json
{
  "question": "什么是菩萨戒？",
  "answer": "菩萨戒是大乘佛教中菩萨修行所持的戒律……",
  "source": "《梵网经》《瑜伽师地论》"
}
```

**代码里解析（一行）**：

```python
import json
result = json.loads(api_response)
print(result["answer"])
```

**易错点**：AI 偶尔会在 JSON 前后加 ```json 标记，解析前先 `strip` 一下：

```python
response = response.strip().removeprefix("```json").removesuffix("```").strip()
result = json.loads(response)
```

**对应今天要写的脚本**：`prompt_json.py`

---

## 三、DeepSeek API 调用模板（直接复制用）

```python
import os
import json
import urllib.request

API_URL = "https://api.deepseek.com/chat/completions"
API_KEY = os.environ["DEEPSEEK_API_KEY"]

def ask(system_prompt, user_message, model="deepseek-v4-flash"):
    """封装 DeepSeek 调用，返回 response 文本"""
    data = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3  # 稳定输出，JSON 场景用更低
    }).encode()

    req = urllib.request.Request(API_URL, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    })

    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
    return body["choices"][0]["message"]["content"]

# 使用示例
if __name__ == "__main__":
    system = "你是一个简洁的助手，回答不超过30字。"
    user = "什么是Python？"
    print(ask(system, user))
```

---

## 四、避坑清单（新手常犯 5 个错）

| 坑 | 现象 | 解法 |
|----|------|------|
| **system prompt 写太虚** | AI 输出跑偏 | 不要说"你是一个 AI 助手"，要说"你是 XX 领域的专家，回答必须包含 A/B/C"，必须加示例+格式 |
| **temperature 默认值太高** | JSON 格式不稳定 | 结构化输出时设 `temperature=0.1~0.3` |
| **prompt 中英文混写** | 部分模型对中文指令效率低 | 关键指令尝试英文表达 |
| **没做错误处理** | JSON 解析崩了整段程序就挂 | JSON 场景永远用 `try/except json.JSONDecodeError` 包裹 |
| **把示例当背景知识** | 模型把示例内容当真 | Few-shot 只是格式示范，不是让你把整篇文章塞进去 |

---

## 五、今日练习（3 个脚本）

| 脚本 | 练哪个技巧 | 核心挑战 |
|------|----------|--------|
| `prompt_few_shot.py` | Few-shot | 写 3 个戒律问答示例，让 AI 回答新问题 |
| `prompt_cot.py` | CoT | 让 AI 先解释戒律含义，再给结论 |
| `prompt_json.py` | 结构化输出 | 返回 `{question, answer, source}` |

所有脚本用上面的 `ask()` 模板，替换 `system_prompt` 和 `user_message` 即可。

---

## 六、一个完整可运行的 Few-shot 示例

```python
import os, json, urllib.request

API_URL = "https://api.deepseek.com/chat/completions"
API_KEY = os.environ["DEEPSEEK_API_KEY"]

# ---- 核心：写好 system prompt ----
SYSTEM = """你是戒律问答专家。严格参照以下示例格式回答。

示例1：
问：什么是五戒？
答：五戒是不杀生、不偷盗、不邪淫、不妄语、不饮酒。
出处：《长阿含经》

示例2：
问：不杀生戒的范围？
答：包括不杀人、不杀动物、不教人杀、不见杀随喜。
出处：《四分律》卷一

示例3：
问：犯戒后如何忏悔？
答：轻戒对首忏悔（向一位清净比丘发露），重戒需羯磨法。
出处：《四分律》忏悔犍度

请回答用户的新问题。"""

def ask(system, user):
    data = json.dumps({
        "model": "deepseek-v4-flash",
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
        body = json.loads(resp.read())
    return body["choices"][0]["message"]["content"]

if __name__ == "__main__":
    q = "不饮酒戒有哪些开缘情况？"
    print("问题:", q)
    print("回答:", ask(SYSTEM, q))
```
