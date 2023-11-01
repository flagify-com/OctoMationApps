# -*- coding: utf-8 -*-
import requests
import json

def http_request(params, assets, context_info):
    """HTTP请求"""

    # URL服务器，如：https://user:pass@example.com:8080
    SERVER = params["SERVER"]
    # URL路径，如：/user/info，默认为：/
    PATH = "/" if "PATH" not in params.keys() or params["PATH"] == "" else params["PATH"]
    # URL请求参数(不带?，需自行做好URL Encode，如：user=Chris&comment=I%20love%20OctoMation）
    QUERY = ""
    if "QUERY" in params.keys() and params["QUERY"] != "" and params["QUERY"] is not None: QUERY= params["QUERY"]
    # HTTP请求头中的Content-Type，默认：application/json
    CONTENT_TYPE = "application/json" if "CONTENT_TYPE" not in params.keys() or params["CONTENT_TYPE"] == "" else params["CONTENT_TYPE"]
    # 自定义HTTP头，KEY:VALUE，按行填写。
    HEADER = ""
    if "HEADER" in params.keys() and params["HEADER"] != "" and params["HEADER"] is not None: HEADER= params["HEADER"]
    # HTTP请求体（Form模式需要自行URL Encode）
    BODY = ""
    if "BODY" in params.keys() and params["BODY"] != "" and params["BODY"] is not None: BODY= params["BODY"]
    # HTTP请求方法，默认：GET
    METHOD = "GET" if "METHOD" not in params.keys() or params["METHOD"] == "" else params["METHOD"]

    # 代理服务器
    PROXY = None
    if "PROXY" in params.keys() and params["PROXY"] != "" and params["PROXY"] is not None: 
        PROXY= {
            "http": params["PROXY"].strip(),
            "https": params["PROXY"].strip()
        }
    
    VERIFY_SSL = True if "VERIFY_SSL" not in params.keys() or params["VERIFY_SSL"] == "" else bool(params["VERIFY_SSL"])
    ALLOW_REDIRECTS = True if "ALLOW_REDIRECTS" not in params.keys() or params["ALLOW_REDIRECTS"] == "" else bool(params["ALLOW_REDIRECTS"])
    TIMEOUT = 60 if "TIMEOUT" not in params.keys() or params["TIMEOUT"] == "" else int(params["TIMEOUT"])

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"http_response_code": 0, "http_response_text": ""}}

    '''添加函数实现
    
    '''
    # 防止手抖
    SERVER = SERVER.strip()
    if SERVER.endswith('/'):
        SERVER = SERVER[:-1]
    PATH = PATH.strip()
    if PATH != "/" and not PATH.startswith('/'):
        PATH = f"/{PATH}"
    QUERY = QUERY.strip()
    if QUERY.startswith('?'):
        QUERY = QUERY[1:]

    # 拼接完整URL
    url = f"{SERVER}{PATH}"
    if QUERY != "":
        url = f"{SERVER}{PATH}?{QUERY}"
    METHOD = METHOD.strip().upper()
    
    # 准备HTTP HEAD字典
    headers = {}
    if CONTENT_TYPE != "":
        headers['content-type'] = CONTENT_TYPE
    for headline in HEADER.split("\n"):
        if ':' in headline:
            key = headline.split(':')[0].strip()
            value = headline.split(':')[-1].strip()
            if key != "" and value != "":
                headers[key.lower()] = value.lower()
    
    try:
        if METHOD in ('POST', 'PUT'):
            res = requests.request(METHOD, url=url, headers=headers, data=BODY.encode(), allow_redirects=ALLOW_REDIRECTS, proxies=PROXY, verify=VERIFY_SSL, timeout=TIMEOUT)
            json_ret['data']['http_response_code'] = res.status_code
            json_ret['data']['http_response_text'] = res.text
        else:
            res = requests.request(METHOD, url=url, headers=headers, allow_redirects=ALLOW_REDIRECTS, proxies=PROXY, verify=VERIFY_SSL, timeout=TIMEOUT)
            json_ret['data']['http_response_code'] = res.status_code
            json_ret['data']['http_response_text'] = res.text
        
        if json_ret['data']['http_response_code'] in (200, 201):
            json_ret['msg'] = "请求发送成功，请确认返回结果:)"
        else:
            json_ret['msg'] = "可能请求失败，请检查错误信息:("
        
    except Exception as e:
        json_ret['code']= -1
        json_ret["msg"] = str(e)

    return json_ret

if __name__ == "__main__":
    params = {
        "SERVER": "https://www.google.com/",
        "PROXY": "http://127.0.0.1:3128",
        "VERIFY_SSL": True
    }
    print(http_request(params, None, None))