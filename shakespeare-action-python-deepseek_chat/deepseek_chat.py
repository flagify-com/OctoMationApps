# -*- coding: utf-8 -*-

import requests

def deepseek_chat(params, assets, context_info):
    """LLM对话"""
    # 获取 token
    token = assets["token"]
    
    # 获取消息内容
    message = params["message"]
    
    # 使用的模型
    model = "deepseek-chat" if "model" not in params.keys() or params["model"] == "" else params["model"]
    
    # 最大 token 数
    max_tokens = 4096 if "max_tokens" not in params.keys() or params["max_tokens"] == "" else params["max_tokens"]
    
    # 温度参数（可选，默认为 1.0）
    temperature = 1.0 if "temperature" not in params.keys() or params["temperature"] == "" else params["temperature"]
    
    # 返回值初始化
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "id": "",
            "choices": [],
            "model": ""
        }
    }

    # 构造请求头
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 构造请求体
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": message}],  # 当前消息
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        # 发送 POST 请求
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        data = response.json()

        # 提取返回数据
        json_ret["data"]["id"] = data.get("id", "")
        json_ret["data"]["choices"] = data.get("choices", [])
        json_ret["data"]["model"] = data.get("model", "")

    except requests.exceptions.RequestException as e:
        # 请求失败时设置错误信息
        json_ret["code"] = 500
        json_ret["msg"] = f"请求失败: {str(e)}"

    return json_ret