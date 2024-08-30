# -*- coding: utf-8 -*-
from app_sdk.globalType import HEADERS
from app_sdk.httpTools import HTTP
from app_sdk.utils.formatConversion import verify_json,str_to_json

def http_requests(params, assets, context_info):
    """HTTP请求"""

    # HTTP请求的url
    url = params["url"]
    # HTTP请求的请求头
    headers=""
    if "headers" in params.keys() :
        headers = params.get("headers", HEADERS.NONE)
    # HTTP请求的SSL验证
    verify = params.get("ssl_verify", False)
    # HTTP请求的请求体
    data = params.get("data", None)
    proxies = params.get("proxy", None)
    method = "GET" if "method" not in params.keys() or params["method"] == "" else params["method"]

    # 返回值
    json_ret = {"code": 500, "msg": "","data": {"status_": 999, "data": {}, "text": ""}}

    '''添加函数实现
    
    '''
    h = HTTP()
    try:
        if type(headers) == str and headers is not None and headers !='':
            headers = headers.replace("'", '"')
            x = str_to_json(headers)
            print(type(x))
            h.headers = x
        elif type(headers) == dict:
            h.headers = headers
        else:
            h.headers=None
        h.verify = verify
        if verify_json(data):
            json_ret = h.req(method, url=url, body=None, json_data=data)
        else:
            json_ret = h.req(method, url=url, body=data, json_data=None)

        del h
        if json_ret.get("data",{}).get("content", None) is not None:
            del json_ret['data']['content']
    except Exception as e:
        json_ret={
            "code": 500, "msg": str(e)
        }
    return json_ret 