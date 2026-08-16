# Java 转 Python 核心差异速查表

> 面向有 Java/PHP 经验的开发者，只讲差异，不讲废话。

---

## 目录

- [1. 缩进规则：用空格代替花括号](#1-缩进规则用空格代替花括号)
- [2. 动态类型 vs 静态类型](#2-动态类型-vs-静态类型)
- [3. 列表推导式（Python 独有）](#3-列表推导式python-独有)
- [4. 函数定义与参数传递](#4-函数定义与参数传递)
- [5. 异常处理的语法差异](#5-异常处理的语法差异)
- [附加：其他高频差异](#附加其他高频差异)
- [练习题](#练习题)

---

## 1. 缩进规则：用空格代替花括号

Python **没有 `{}`**，代码块完全由缩进定义。同一代码块的缩进必须一致，官方推荐 4 个空格。

| 语言 | 代码块界定方式 |
|------|---------------|
| Java | `{}` 花括号 |
| PHP | `{}` 花括号 |
| Python | **缩进**（IndentationError 是常见新手坑） |

### 对比示例

**Java：**

```java
if (x > 0) {
    System.out.println("positive");
    if (x > 10) {
        System.out.println("large");
    }
}
```

**PHP：**

```php
if ($x > 0) {
    echo "positive";
    if ($x > 10) {
        echo "large";
    }
}
```

**Python：**

```python
if x > 0:
    print("positive")
    if x > 10:
        print("large")
```

> 注意：Python 中 `:` 是必须的，缩进不一致会直接报错。

---

## 2. 动态类型 vs 静态类型

Python 是**动态类型**语言，变量不需要声明类型，运行时才确定。Java 是静态类型，编译时检查。

### 对比示例

**Java（静态类型）：**

```java
String name = "Alice";      // 必须声明类型
int age = 30;                // 类型不可变
// name = 30;                // 编译错误
```

**PHP（动态类型，有类型标注）：**

```php
$name = "Alice";             // 动态类型
$age = 30;                   // 同个 $ 前缀
// PHP 8.0+ 可加类型声明，但不强制
function greet(string $name): string {
    return "Hello, $name";
}
```

**Python（动态类型）：**

```python
name = "Alice"               # 无需类型声明
age = 30                     # 变量可随时指向不同类型
name = 30                    # 完全合法

# Python 3.5+ 支持可选的类型提示（type hints），不强制
def greet(name: str) -> str:
    return f"Hello, {name}"
```

| 特性 | Java | PHP | Python |
|------|------|-----|--------|
| 类型检查 | 编译时 | 运行时（可选声明） | 运行时 |
| 变量声明 | `Type name = value` | `$name = value` | `name = value` |
| 类型提示 | 内置强制 | PHP 8.0+ 可选 | 3.5+ 可选，需 mypy 检查 |

---

## 3. 列表推导式（Python 独有）

Python 最强大的特性之一：一行代码完成「循环 + 过滤 + 映射」。Java 需 Stream API，PHP 需 array_map/array_filter 组合。

### 对比：筛选偶数并平方

**Java（Stream API）：**

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6);
List<Integer> result = numbers.stream()
    .filter(n -> n % 2 == 0)
    .map(n -> n * n)
    .collect(Collectors.toList());
// [4, 16, 36]
```

**PHP：**

```php
$numbers = [1, 2, 3, 4, 5, 6];
$result = array_map(
    fn($n) => $n * $n,
    array_filter($numbers, fn($n) => $n % 2 == 0)
);
// [4, 16, 36]
```

**Python：**

```python
numbers = [1, 2, 3, 4, 5, 6]
result = [n * n for n in numbers if n % 2 == 0]
# [4, 16, 36]
```

### 更多推导式

```python
# 字典推导式
squares = {n: n * n for n in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 集合推导式
unique_lengths = {len(word) for word in ["hi", "hello", "world"]}
# {2, 5}

# 嵌套推导式（展平二维列表）
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6]
```

---

## 4. 函数定义与参数传递

Python 函数参数体系比 Java/PHP 更灵活：支持**默认参数、关键字参数、可变参数（*args）、可变关键字参数（**kwargs）**。

### 默认参数

**Java（用方法重载模拟）：**

```java
public String greet(String name) {
    return greet(name, "Hello");
}
public String greet(String name, String prefix) {
    return prefix + ", " + name;
}
```

**PHP：**

```php
function greet($name, $prefix = "Hello") {
    return "$prefix, $name";
}
```

**Python：**

```python
def greet(name, prefix="Hello"):
    return f"{prefix}, {name}"
```

> 注意：Python 默认参数只求值一次，可变对象（如列表）作默认值会出 bug：
> ```python
> # 错误示范
> def add_item(item, items=[]):  # 多次调用共享同一个 list
>     items.append(item)
>     return items
> # 正确做法
> def add_item(item, items=None):
>     if items is None:
>         items = []
>     items.append(item)
>     return items
> ```

### 关键字参数（调用时指定参数名）

```python
def order(product, quantity=1, discount=0):
    return f"{product} x{quantity}, discount={discount}%"

# 可按任意顺序传参
order(discount=10, product="book")  # 'book x1, discount=10%'
```

### *args 与 **kwargs

| 语法 | 含义 | Java/PHP 等价 |
|------|------|--------------|
| `*args` | 接收任意数量的**位置参数**（元组） | Java 可变参数 `String... args` |
| `**kwargs` | 接收任意数量的**关键字参数**（字典） | 无直接等价，通常用 Map |

```python
# *args：类似 Java 的 String...
def sum_all(*args):
    return sum(args)

sum_all(1, 2, 3, 4)  # 10

# **kwargs：Python 独有
def build_url(base, **params):
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{base}?{query}"

build_url("/search", q="python", page=2)
# '/search?q=python&page=2'

# 组合使用
def api_call(endpoint, *args, **kwargs):
    print(f"Endpoint: {endpoint}")
    print(f"Positional: {args}")
    print(f"Keyword: {kwargs}")

api_call("/users", "GET", "v2", timeout=30, retry=3)
```

---

## 5. 异常处理的语法差异

Python 的关键词是 `try/except/else/finally`，注意是 **except** 不是 **catch**。Python 还有 `else` 分支：无异常时执行。

### 对比示例

**Java：**

```java
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Error: " + e.getMessage());
} finally {
    System.out.println("Cleanup");
}
// Java 有 checked exception：IOException 必须声明 throws 或 catch
```

**PHP：**

```php
try {
    $result = 10 / 0;
} catch (DivisionByZeroError $e) {
    echo "Error: " . $e->getMessage();
} finally {
    echo "Cleanup";
}
```

**Python：**

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
else:
    print(f"Result: {result}")  # 无异常时执行（Java/PHP 无此分支）
finally:
    print("Cleanup")
```

### 关键差异

| 特性 | Java | PHP | Python |
|------|------|-----|--------|
| 关键词 | `catch` | `catch` | **`except`** |
| Checked Exception | 有 | 无 | 无 |
| else 分支 | 无 | 无 | **有**（无异常时执行） |
| 抛出异常 | `throw new Xxx()` | `throw new Xxx()` | **`raise Xxx()`** |
| 捕获多个异常 | `catch (A \| B e)` | `catch (A \| B $e)` | `except (A, B) as e` |
| 自定义异常 | `extends Exception` | `extends \Exception` | `class MyErr(Exception): pass` |

### 抛出异常

```python
# Python
def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b
```

```java
// Java
public int divide(int a, int b) {
    if (b == 0) {
        throw new IllegalArgumentException("除数不能为零");
    }
    return a / b;
}
```

---

## 附加：其他高频差异

### 布尔值与空判断

```python
# Python 的 Falsy 值：None, False, 0, 0.0, "", [], {}, set()
if not items:          # 等价于 Java 的 items == null || items.isEmpty()
    print("空")

# None 是 Python 的 null
result = None
if result is None:     # 用 is，不是 ==
    print("无结果")
```

### 字符串格式化

```python
name = "World"
# f-string（Python 3.6+，推荐）
f"Hello, {name}"

# 等价于
"Hello, {}".format(name)     # Java: String.format("Hello, %s", name)
"Hello, %s" % name           # PHP: "Hello, $name"
```

### 三元运算符

```java
// Java
String s = x > 0 ? "positive" : "negative";
```

```python
# Python 语序不同
s = "positive" if x > 0 else "negative"
```

### 循环与迭代

```python
# Python 的 for 直接遍历对象（类似 Java for-each / PHP foreach）
for item in items:
    print(item)

# 需要索引时用 enumerate
for i, item in enumerate(items):
    print(f"{i}: {item}")

# 同时遍历两个列表用 zip
for a, b in zip(list_a, list_b):
    print(a, b)
```

---

## 练习题

### 练习 1：列表推导式

将以下 Java 代码用 Python 重写：

```java
List<Integer> nums = Arrays.asList(3, 7, 9, 12, 15, 18, 21);
List<Integer> result = nums.stream()
    .filter(n -> n % 3 == 0)
    .map(n -> n * 2)
    .sorted(Comparator.reverseOrder())
    .collect(Collectors.toList());
```

要求：用**一行列表推导式**完成「筛选能被 3 整除的数 → 翻倍 → 降序排列」。

---

### 练习 2：函数参数（*args / **kwargs）

实现 Python 函数 `describe_person(name, *hobbies, **details)`：

- `name`：必填，姓名
- `*hobbies`：任意数量爱好
- `**details`：任意键值对附加信息

调用示例与期望输出：

```python
result = describe_person("Alice", "coding", "reading", age=30, city="Beijing")
print(result)
# {
#     "name": "Alice",
#     "hobbies": ["coding", "reading"],
#     "age": 30,
#     "city": "Beijing"
# }
```

---

### 练习 3：异常处理（try/except/else）

实现函数 `safe_read_file(filepath, default="")`：

- 尝试读取文件内容并返回
- 文件不存在时返回 `default`
- 其他异常向上抛出
- 使用 `try/except/else` 结构，在 `else` 分支中打印 `"读取成功: {文件路径}"`

提示：Python 读文件用 `with open(filepath, "r", encoding="utf-8") as f: return f.read()`

---

## 参考答案

### 练习 1：列表推导式

```python
nums = [3, 7, 9, 12, 15, 18, 21]
result = sorted([n * 2 for n in nums if n % 3 == 0], reverse=True)
# [42, 36, 30, 24, 18, 6]
```

> 解析：列表推导式 `[n * 2 for n in nums if n % 3 == 0]` 一步完成筛选+映射，外层 `sorted(..., reverse=True)` 降序排列。

### 练习 2：函数参数

```python
def describe_person(name, *hobbies, **details):
    result = {"name": name, "hobbies": list(hobbies)}
    result.update(details)
    return result

# 测试
result = describe_person("Alice", "coding", "reading", age=30, city="Beijing")
print(result)
# {'name': 'Alice', 'hobbies': ['coding', 'reading'], 'age': 30, 'city': 'Beijing'}
```

> 解析：`*hobbies` 收集为元组，用 `list()` 转列表；`**details` 收集为字典，用 `update()` 合并。

### 练习 3：异常处理

```python
def safe_read_file(filepath, default=""):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return default
    else:
        print(f"读取成功: {filepath}")
        return content
    # 其他异常（PermissionError 等）不做处理，自动向上抛出

# 测试
print(safe_read_file("不存在.txt", "默认内容"))
# 输出 "默认内容"（文件不存在，返回 default）

# 创建测试文件后：
# 输出 "读取成功: test.txt" 和文件内容
```

