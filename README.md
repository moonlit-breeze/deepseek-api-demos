# DeepSeek API Demos

三种语言调用 DeepSeek API 的示例，向模型提问"什么是无我"，打印 AI 回答。

## 项目结构

```
├── java/          # Java + Maven
├── php/           # PHP
├── python/        # Python（纯标准库）
└── README.md
```

## 运行方式

### 前置条件

注册 [DeepSeek API](https://platform.deepseek.com) 并获取 API Key。

### Java

```bash
cd java
set DEEPSEEK_API_KEY=sk-你的key
mvn exec:java
```

### PHP

```bash
cd php
set DEEPSEEK_API_KEY=sk-你的key
php FoQaPHP.php
```

### Python

```bash
cd python
set DEEPSEEK_API_KEY=sk-你的key
python FoQaPython.py
```

> PowerShell 用户请将 `set` 替换为 `$env:DEEPSEEK_API_KEY = "sk-你的key"`
