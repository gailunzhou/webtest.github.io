<div class="article-meta" style="background: #f0f8ff; padding: 15px; border-left: 4px solid #2196f3; margin-bottom: 20px; border-radius: 4px;">
<p style="margin: 0; color: #666; font-size: 0.9em;">
<strong>📅 发布日期:</strong> 年-月-日 &nbsp;|&nbsp;
<strong>👤 作者:</strong> teriyakisushi &nbsp;|&nbsp;
<strong>📁 分类:</strong> 技术笔记 &nbsp;|&nbsp;
<strong>🏷️ 标签:</strong> LLM&API
</p>
</div>

# API与LLM调用入门指南

## 1. API介绍

### 1.1 什么是API？

API（Application Programming Interface，应用程序接口）是服务提供方（如 OpenAI）对外公开的一个“调用入口”，你可以通过这个入口，远程发送请求，获取模型的生成结果。

假设我们本地写了一个非常棒的相加函数：

```python
# 获取两数之和
def plus_num(num1: int, num2: int) -> num:
    return num1 + num2
```

我们在本地直接调用 `plus_num` 就可以直接得到结果，这很棒，如果我想让别人随时随地都能使用，而不是需要将代码复制到本地然后重新跑一遍呢？

那就让这个函数通过网络暴露出来，即使在别的电脑、别的网络环境也能通过这个接口去获取结果，这就是API的本质，我们不需要关心如何暴露接口，你只需知道调用API的过程是：

**通过一个网址（URL）+ 请求，把参数发过去，服务器返回结果。**

如果有一个远程服务已经提供了我们刚才写好的加法功能，我们只需要向这个地址发送请求，就能得到结果。

假设我们已经暴露了这个接口URL为：`http://myservice.com/plus`

那按照函数的入参要求，需要提供 `num1` 和 `num2` 这两个参数才能得到结果，
我们可以向它发送请求的参数为：

```json
{
    "num1": 3,
    "num2": 5
}
```

那服务器会响应并返回结果为 8，这就是API调用的过程。

### 1.2 如何请求？

这里不会细讲计算机网络的知识，你只需知道：
请求（Request）是要通过 GET/POST 方式，附带的参数需要包含以下内容：

#### Header

请求头包含一些元信息，告诉服务器你是谁、你发送的内容是什么格式。

比如我们前面上线的加法API，我需要传参 json 格式的参数 num1 和 num2，

那Header就要包含：

`Content-Type: application/json`

Content-Type有很多类型，如图片的 image/jpeg ，我们这里只说json，这是一个常用的数据格式，
它的结构是键值对的集合，类似于 Python 中的字典。

- 键 (Key)：必须是字符串，用双引号包裹。
- 值 (Value)：可以是字符串、数字、布尔值（true / false）、数组（[]）或者另一个 JSON 对象（{}）

```json
{
    "name": "小明", // 字符串
    "age": 18, // 数字
    "isStudent": true, // 布尔值
    "courses": ["数学", "英语"], // 数组
    "info": { "id": "001" } // 对象
}
```

除了 Content-Type ，另一个非常重要的 Header 是 Authorization （授权）；大多数公开的 API 都需要验证调用者的身份，以防止被滥用。Authorization 请求头就是用来存放身份凭证的。

例如，调用 OpenAI 的 API 时，你需要提供一个密钥（API Key），请求头就会是这样：

`Authorization: Bearer sk-xxxxxxxxxxxxxxxxxxxxxx`

!!! success "Success"
    这里的 `sk-xxxxxxxxxxxxxxxxx` 就是用来验证你身份的密匙，Bearer 是一种常用的授权类型。

#### Body

请求体（Body）是请求中发送给服务器的主要数据。对于我们 plus 的例子，请求体就是我们想要相加的两个数字，以 json 格式表示：

```json
{
    "num1": 3,
    "num2": 5
}
```

前面我们提到了 GET 方法，但请注意，当我们像上面那样通过请求体（Body）发送 json 数据时，通常使用的请求方法是 POST，而不是 GET。

#### Get方法

GET：通常用于获取数据。参数一般会直接拼接在 URL 后面，例如

`http://myservice.com/plus?num1=3&num2=5` 它没有请求体。

#### Post方法

POST：通常用于提交或创建数据。参数会放在请求体（Body）中发送，这样可以发送更复杂、更长的结构化数据（比如我们的 json）。

至此，你已经了解了调用一个 API 的基本要素包含如下参数：

- **URL：**API 的地址。
- **Method：**请求方法，如 GET 或 POST。
- **Headers：**请求的元信息，如内容格式 Content-Type 和身份凭证 Authorization。
- **Body：**要发送给服务器的具体数据（主要用于 POST 请求）。

## 2. 调用LLM的API

### 2.1 SDK安装

相信通过上篇文章你已经对API的使用已经有了一定的了解，那我们就直奔主题，调用 DeepSeek的API实现本地对话效果。

首先确保你的 Python 解释器版本为 3.8+ （推荐 3.10+）

我们先安装OpenAI封装好的SDK库，它将复杂的参数和request流程都打包好了，开箱即用。

***Tips***

*建议先创建虚拟环境隔离全局包 python -m venv .venv*

使用命令行(即终端 Windows：CMD/PowerShell；Mac/Linux：Terminal)安装：

```bash
pip install openai
```

若有依赖冲突建议创建虚拟环境后再安装，还是不行问AI寻找解决方案。

### 2.2 编写第一个对话框序

以官方文档写法作为例子：

```python
from openai import OpenAI

client = OpenAI(
    api_key="<your API key>", # 用作身份验证
    base_url="https://api.deepseek.com" # 我们要调用DeepSeek的API，所以url就必须是ds的
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello"},
],
    max_tokens=1024,
    temperature=0.7,
    stream=False
)
print(response.choices[0].message.content)
```

修改 `api_key` 参数，这里可以用我的：`sk-13d9f0321ba6d49e4b57f9f44e9f1caad` 直接运行后可以看到LLM会返回一行文本内容示例如下图：

![Introduction to LLM APIs01](images/2025-11-12-Introduction%20to%20LLM%20APIs/Introduction%20to%20LLM%20APIs01.png)

让我们详细解释一下：

1. `OpenAI` 是一个类，通过 `api_key` 和 `base_url` 这两个基础参数去创建这个实例，这样就能调用LLM的API了，就像我们上一篇说的，发送请求需包含目标地址、身份验证的key和请求内容。
2. `chat.completions.create` 这个方法封装好了整个请求的流程，你只需要填写有关的请求体内容（参数）就行了，相关参数需要参照官方的SDK说明。
3. 程序最后 `print` 的是LLM返回的结果，需要注意的是调用LLM的API对话返回的结果并不是纯文本，而是包含各种信息的 json ，下面会细说。

### 2.3 请求接口

回顾上面的代码，我们知道发送请求需要携带的参数有比如 model, messages, stream 等，
它们的具体含义由于LLM的差异，这里建议直接翻看官方提供的API文档。

其中标红的 required 字段为必须填入的参数，我这里只解释最基础的
model, messages, stream：

**model:**

调用对话所需的模型，填写是要看官方提供的模型列表。
这里用的DeepSeek作演示，官方提供了两种模型 `deepseek-chat` 和 `deepseek-reasoner`。
后者是深度思考模式，返回结果包含reasoning过程。

**messages:**

messages 是对话的核心参数，它定义了整个对话的上下文；
这个参数是一个消息字典组成的列表，每个字典包含两个关键字段：

```json
{
    "role": "角色类型",
    "content": "具体内容"
}
```

角色类型（role）有三种：

1. **system：**设定AI助手的角色和基础行为准则（如"You are a helpful assistant"）
    1. 通常作为第一条消息出现
    2. 对整个对话有全局性影响
2. **user：**用户输入的内容，就像上方示例的"Hello"
3. **assistant：**AI之前的回复内容（用于多轮对话上下文）

**消息顺序至关重要：**

消息列表必须严格按对话时间顺序排列，例如：

```python
messages = [
    {"role": "system", "content": "你是个精通C语言的专家"}, # 系统提示词
    {"role": "user", "content": "如何用C语言比较两个数的大小？"}, # 用户提问对话
    {"role": "assistant", "content": "可以使用 std::max() 函数"}, # LLM的回复
    {"role": "user", "content": "那怎么给一个数组排序"}, # 基于上轮对话继续提问
]
```

📍 **Tips：**每次请求都需要包含完整对话历史，API本身不保存对话状态。

我相信你可以看出来，要实现多轮对话的话，只需要把对话历史直接追加到messages列表里，然后再进行对话请求，就能关联上下文，相当于LLM产生"记忆"了，这就是LLM实现上下文联想的核心。

!!! warning "Warning"
    有些LLM请求所需的 messages 列表的条目必须要保持奇数倍以保持格式规范。

    剩下的更多请求体参数如 temperature，frequency_penalty 等请自行查阅API文档。

### 2.4 响应内容

上面说过，LLM返回的结果并不是纯文本，而是带有各种字段的 json 格式。

现在打开 API文档，在右侧的Mock栏输入上面提供的 api_key 并填入Auth字段：

**REQUEST**

```json
{
    "messages": [
    {
    "content": "You are a helpful assistant",
    "role": "system"
    },
    {
    "content": "Hello",
    "role": "user"
    }
],
"model": "deepseek-chat",
"frequency_penalty": 0,
"max_tokens": 2048,
"presence_penalty": 0,
"response_format": {
    "type": "text"
    },
    "stop": null,
    "stream": false,
    "stream_options": null,
    "temperature": 1,
    "top_p": 1,
    "tools": null,
    "tool_choice": "none",
    "logprobs": false,
    "top_logprobs": null
}
```

这个界面能很好的反映请求体所携带的参数列表和返回的内容——完整流程！

然后发送请求，看看Response返回了什么：

```json
{
    "id": "ea5b6f3e-e1a3-480a-8f28-2e0f579f2815",
    "object": "chat.completion",
    "created": 1752846137,
    "model": "deepseek-chat",
    "choices": [
    {
    "index": 0,
    "message": {
    "role": "assistant",
    "content": "Hello! How can I assist you today? 😊"
    },
    "logprobs": null,
    "finish_reason": "stop"
    }
],
"usage": {
    "prompt_tokens": 9,
    "completion_tokens": 11,
    "total_tokens": 20,
    "prompt_tokens_details": {
    "cached_tokens": 0
    },
    "prompt_cache_hit_tokens": 0,
    "prompt_cache_miss_tokens": 9
    },
    "system_fingerprint": "fp_8802369eaa_prod0623_fp8_kvcache"
}
```

你会注意到"文本"内容在 `choices` 字段的 `message` 里，这就是LLM的纯文本回复。

其他字段不介绍了，API文档里 Responses 解释的很清楚。

所以，要想看到LLM只返回对话答案（内容）而不是这么一大串数据，就需要剔除其他无关的字段。
示例程序已经给了一个不错的方案：

```python
print(response.choices[0].message.content)
```

意思是只输出 `choices` 字段中 `index` 为 0 的 `message` 列表中的内容，即纯文本内容。

### 2.5 总结

相信你已经能理解调用LLM的过程了：

- 填写目标 url 和 api_key
- 编辑请求体所需携带的参数
- LLM响应内容

不妨试着新建一个python程序，
新增一些参数比如 temperature、修改role为 system 的提示词，看看返回的效果？

这次演示的内容是单次对话且上下文不会被LLM记忆，接下来让我们实现能多轮对话的简易对话框序，让LLM能记住你前几次说了什么。

## 3. 实现多轮对话CLI

### 3.1 多轮对话的原理

多轮对话的核心在于维护对话上下文。在每次交互中，我们需要：

1. **保存历史对话：**将用户输入和AID回复都添加到对话历史中
2. **传递完整上下文：**每次请求API时发送全部对话历史
3. **管理对话状态：**处理对话开始、结束和异常情况

这种设计让AI能够理解之前的对话内容，实现连贯的对话体验；梳理一下过程可以写出很清晰的伪代码：

```python
while True: # 必须让对话在循环内进行否则单次对话就退出了  
    user_input() # 用户输入文本内容  
    messages.add(user_input) # 将用户输入的东西加进message列表  
    response = send_to_llm(...message) # 将完整对话列表发给LLM并获取回复  
    ai_reply = 从response筛选出来纯文本  
    messages.add (ai_reply) # 将LLM的纯文本回复也加到message列表  
```

### 3.2 简易的LLM对话CLI程序

基于上面的过程，我们可以快速写出这个程序（相关过程已经单独封装成函数了，见注释）：

```python
from openai import OpenAI

# 全局变量  
api_key = "sk-7a9a9de83568404bac7b8cd1570ec239"  
base_url = "https://api.deepseek.com"

# 使用的对话模型  
model = "deepseek-chat"

# 构造初始的对话列表  
messages = [  
    {"role": "system", "content": "You are a helpful assistant"},  
    {"role": "user", "content": "你好"},  
    {"role": "assistant", "content": "你好，有什么可以帮助您的?"},  
]

# 将当前消息添加到对话列表中  
def add_message(new_msg: list) -> list:  
    messages.append(new_msg)  
    return messages  

# 提取回复中的文本内容
def get_result(response: dict) -> str:
    return response.choices[0].message.content

# 提取用户的输入并构建为message格式
def user_input() -> str:
    ask = input("用户: ")
    ask_msg = {"role": "user", "content": ask}
    return ask_msg

# 对话流程
def chat_completion(client: OpenAI) -> None:
    # 用户输入
    add_message(user_input())

    # 将对话内容发送给LIM并获取响应结果
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
        stream=False
    )

    # 将AI回复添加到对话列表中
    ai_reply = {"role": "assistant", "content": get_result(response)}
    add_message(ai_reply)

# 程序入口
if __name__ == "__main__":
    # 初始化
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    # 进入对话
    while True:
        chat_completion(client)
        print("DeepSeek: " + messages[-1]['content'])
```

看一下LIM能否记住对话内容：

!!! note "text"
    Administrator 32 python .vexample.py

    用户：我刚才说了什么？

    DeepSeek：你刚才说的是："你好"，然后我回复了你："你好，有什么可以帮助您的?"。这是我们对话的开始部分。如果你需要回填其他的词，可以告诉我，我会帮你回忆。

    用户：我刚才又说了什么？
    DeepSeek：你刚才说的是："我刚才说了什么？"，而这是我之前的回答内容。

    现在，你是新的提问吧："我刚才又说了什么？"

    如果您要回填更早的对话内容，可以告诉我是你知道，我会帮你梳理哦！

### 3.3 对话管理与异常处理

有时候LLM的响应内容会受网络、用户输入等因素而影响，导致无法正确解析回答，这样的异常状况会导致程序崩溃，为了程序运行的稳定性，有必要为对话过程加上异常捕捉，当抛出异常时可做相应的措施以防程序中断，影响系统的运行；

我们可以使用 Python 的 try...except 语句来包裹可能出错的代码块。<br>
try 块是程序正常运行的部分，except 则是程序出现异常时会进入的部分。

在我们的例子中，网络请求 `client.chat.completions.create(...) `和结果提取` get_result(response) `是最可能发生异常的地方，当异常发生时，我们可以在 except 块中打印错误信息，并让用户重新输入，而不是让整个程序崩溃。

同时，一个健壮的对话框序还应该提供管理功能，例如：

- **退出对话：**允许用户通过特定命令（如 exit 或 quit）正常退出程序。
- **重置对话：**当用户希望开始一个全新话题时，可以清空历史记录。

下面是加入了异常处理和对话管理功能的改进版代码：

```python
from openai import OpenAI  
import sys  

# 全局变量  
api_key = "sk-7a9a9de83568404bac7b8cd1570ec239"  
base_url = "https://api.deepseek.com"  
model = "deepseek-chat"  

# 初始对话，可以只保留一个 system prompt  
initial_messages = [  
    {  
        "role": "system",  
        "content": "You are a helpful assistant."  
    },  
]  

# 复制一份初始对话用于重置  
messages = list(initial_messages)  

# 将当前消息添加到对话列表中  
def add_message(new_msg: dict):  
    messages.append(new_msg)  

# 提取回复中的文本内容  
def get_result(response: dict) -> str:  
    return response.choices[0].message.content  

# 对话流程  
def chat_completion(client: OpenAI):
    try:
        # 将对话内容发送给LLM并获取响应结果
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
            stream=False
        )
        # 提取AI回复并添加到对话列表
        ai_reply_content = get_result(response)
        add_message({"role": "assistant", "content": ai_reply_content})
        # 打印AI的回复
        print("DeepSeek: " + ai_reply_content)

    except Exception as e:
        print(f"发生错误: {e}")
        # 如果出错，移除刚才添加的用户输入，防止污染上下文
        if messages and messages[-1]["role"] == "user":
            messages.pop()

# 程序入口
if __name__ == "__main__":
    # 初始化
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    print("对话开始（输入 'exit' 或 'quit' 退出，输入 'reset' 重置对话）")

    # 进入对话循环
    while True:
        try:
            ask = input("用户: ")
            # 对话管理命令
            if ask.lower() in ["exit", "quit"]:
                print("再见！")
                break
            if ask.lower() == "reset":
                messages = list(initial_messages)
                print("\n[系统] 对话已重置。\n")
                continue

            # 将用户输入添加到对话列表
            add_message({"role": "user", "content": ask})

            # 执行对话
            chat_completion(client)

        except (KeyboardInterrupt, EOFError):
            print("\n再见！")
            sys.exit(0)
```

### 3.4 总结

这一章节扩展了和LLM单次对话的功能，实现多轮对话小demo，当然这只是一个非常简易的程序；但你能在这个基础上实现更强更丰富的系统扩展，比如添加语音识别和播放，更进阶的还有让LLM调用你写的函数/程序实现更复杂的功能，这些可以参考function tools或MCP去实现。


