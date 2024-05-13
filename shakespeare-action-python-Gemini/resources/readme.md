# Gemini问答机器人

## 信息

- 作者：[wzfukui](https://github.com/wzfukui)
- 日期：2024-05-13
- 版本：v1.0
- 语言：Python
- 依赖：网络可达

## 功能

调用Google Gemini API，实现问答机器人。根据用户提交的问题，请求API并返回答案。


## 配置
- key：Gemini API key
- api_host：Gemini API host（推荐是经过反向代理的域名，默认：generativelanguage.googleapis.com）

## 结构

### 输入数据

```json
{
    "question(问题)":"请介绍一下SOAR结束"
}
```

### 输出数据


```json
{
  "msg": "",
  "code": 200,
  "startTime": "2024-05-13 14:11:18",
  "finishTime": "2024-05-13 14:11:31",
  "data": {
    "answer": "**SOAR（安全编排、自动化和响应）**\n\nSOAR 是一种网络安全技术，有助于组织自动化和协调安全操作过程。它将安全编排、自动化和响应功能整合到一个单一的平台中，从而提高安全团队的效率和有效性。\n\n**主要功能：**\n\n,...",
    "err_msg": "success",
    "err_code": 200
  }
}
```

## 单元测试

```
python gemini_unitest.py -v
test_generate_content_api_failure (__main__.TestGenerateContent.test_generate_content_api_failure) ... ok
test_generate_content_happy_path (__main__.TestGenerateContent.test_generate_content_happy_path) ... ok

----------------------------------------------------------------------
Ran 2 tests in 4.151s

OK
```

## Google Gemini API

### API地址

API接口地址：https://ai.google.dev/gemini-api/docs/get-started/rest


## 示例

### 问题1：What is the capital of France?

问题

```bash
curl -H 'Content-Type: application/json' \
-X POST -d '{ "contents":[{ "parts":[{"text": "What is the capital of France?"}]}]}' \
"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=********"
```

答案

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "Paris"
          }
        ],
        "role": "model"
      },
      "finishReason": "STOP",
      "index": 0,
      "safetyRatings": [
        {
          "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
          "probability": "NEGLIGIBLE"
        },
        {
          "category": "HARM_CATEGORY_HATE_SPEECH",
          "probability": "NEGLIGIBLE"
        },
        {
          "category": "HARM_CATEGORY_HARASSMENT",
          "probability": "NEGLIGIBLE"
        },
        {
          "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
          "probability": "NEGLIGIBLE"
        }
      ]
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 7,
    "candidatesTokenCount": 1,
    "totalTokenCount": 8
  }
}
```