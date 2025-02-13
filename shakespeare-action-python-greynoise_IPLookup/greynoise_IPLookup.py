# -*- coding: utf-8 -*-

import requests

def lookup_ip(params, assets, context_info):
    """IP查询"""

    # API Token
    token = assets.get("Token")  # 获取 Greynoise API Token
    if not token:
        return {"code": 400, "msg": "Missing API Token", "data": {}}

    # IP 查询参数
    ip = params.get("IP")
    if not ip or ip == "":
        return {"code": 400, "msg": "Missing or invalid 'IP' parameter", "data": {}}

    # Greynoise API 配置
    GREYNOISE_BASE_URL = "https://api.greynoise.io/v3/community/"
    headers = {
        "Accept": "application/json",
        "key": token
    }

    # 返回值初始化
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "ip": "",
            "noise": "",
            "classification": ""
        }
    }

    try:
        # 构造 Greynoise API 请求 URL
        url = f"{GREYNOISE_BASE_URL}{ip}"

        # 发送 GET 请求到 Greynoise API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应数据
        data = response.json()

        # 提取需要的字段
        json_ret["data"]["ip"] = data.get("ip", "")
        json_ret["data"]["noise"] = data.get("noise", False)
        json_ret["data"]["classification"] = data.get("classification", "")

        # 设置成功消息
        json_ret["msg"] = "Query successful"

    except requests.exceptions.RequestException as e:
        # 处理请求异常
        json_ret["code"] = 500
        json_ret["msg"] = f"Error querying Greynoise API: {str(e)}"

    return json_ret
