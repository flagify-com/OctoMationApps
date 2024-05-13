# -*- coding: utf-8 -*-
import requests
import json

def generateContent(params, assets, context_info):
    """向Gemini提问"""


    # API Key
    key = assets["key"]
    # API主机名
    api_host = "generativelanguage.googleapis.com" if "api_host" not in assets.keys() or assets["api_host"] == "" else assets["api_host"]

    # 问题
    question = params["question"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"answer": "", "err_code": 200, "err_msg": ""}}


    """
    curl -H 'Content-Type: application/json' -X POST \
        -d '{ "contents":[{ "parts":[{"text": "什么是DDoS攻击"}]}]}' \
            "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=***"
    """
    # ..有个bug
    url = "https://{}/v1/models/gemini-pro:generateContent?key={}".format(api_host, key)

    headers = {"Content-Type": "application/json"}

    data = { "contents":[{ "parts":[{"text": question}]}]}

    req = requests.post(url, headers=headers, data=json.dumps(data),timeout=60)
    try:
        if req.status_code == 200:
            json_data = req.json()
            if 'candidates' in json_data.keys() and len(json_data['candidates'])>0:
                json_ret["data"]["answer"] = json_data["candidates"][0]["content"]["parts"][0]["text"]
                json_ret["data"]["err_code"] = 200
                json_ret["data"]["err_msg"] = "success"
            else:
                json_ret["data"]["err_code"] = 500
                json_ret["data"]["err_msg"] = "API无返回"
        else:
            json_ret["data"]["err_code"] = req.status_code
            json_ret["data"]["err_msg"] = req.text
    except Exception as e:
        json_ret["data"]["err_code"] = 500
        json_ret["data"]["err_msg"] = str(e)
        

    return json_ret 

def health_check(params, assets, context_info):
    """健康检查"""

    # API Key
    key = assets["key"]
    # API主机名
    api_host = "generativelanguage.googleapis.com" if "api_host" not in assets.keys() or assets["api_host"] == "" else assets["api_host"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"err_code": 200, "err_msg": "success"}}

    '''添加函数实现
    
    '''
    # curl "https://generativelanguage.googleapis.com/v1/models?key=***"

    url = "https://{}/v1/models?key={}".format(api_host, key)

    req = requests.get(url)

    if req.status_code == 200:
        json_data = req.json()
        if "models" in json_data.keys():
            json_ret["data"]["err_msg"] = "success"
            json_ret["data"]["err_code"] = 200
            json_ret["code"] = 200
    else:
        json_ret["code"] = req.status_code
        json_ret["data"]["err_code"] = req.status_code
        json_ret["data"]["err_msg"] = req.text

    return json_ret 


if __name__ == '__main__':
    params = {"question": "Hi"}
    assets = {
        "key": "GEMINI_API_KEY",
        "api_host": "generativelanguage.googleapis.com"
        }
    context_info = {}
    print(generateContent(params, assets, context_info))
    print(health_check(params, assets, context_info))