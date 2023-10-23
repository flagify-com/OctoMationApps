# -*- coding: utf-8 -*-
import requests

def send_text_message(params, assets, context_info):
    """发送消息到会话ID（或用户ID）"""

    # Telegram Bot Token. 可以通过 @BotFather获取
    bot_token = assets["bot_token"]
    # API地址，支持自定义（魔法地址）
    api_url = "https://api.telegram.org" if "api_url" not in assets.keys() or assets["api_url"] == "" else assets["api_url"]
    Proxies = None
    if 'http_proxy' in assets.keys() and assets['http_proxy'] != '':
        http_proxy = assets['http_proxy']
        Proxies = {
            "http": http_proxy,
            "https": http_proxy
        }
    # Chat Id或者User Id
    chatid = params["chatid"]
    # 文本消息
    text_message = params["text_message"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"success": False}}

    '''添加函数实现
    
    '''
    chat_id = chatid
    message = text_message

    url = f"{api_url}/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, data=data, proxies=Proxies, timeout=30)
        if response.status_code == 200:
            json_res = response.json()
            if 'ok' in json_res.keys() and json_res['ok'] is True:
                json_ret['data']['success'] = True
                json_ret['msg'] = "发送成功"
            else:
                json_ret['code'] = -1
                json_ret['msg'] = "发送失败：{0}".format(response.text)
        else:
            json_ret['code'] = response.status_code
            json_ret['msg'] = "HTTP请求异常：{0}".format(response.status_code)
    except Exception as e:
        json_ret['code'] = -1
        json_ret['msg'] = str(e)

    return json_ret 

def test(params, assets, context_info):
    """测试Telegram服务"""

    # Telegram Bot Token. 可以通过 @BotFather获取
    bot_token = assets["bot_token"]
    # API地址，支持自定义（魔法地址）
    api_url = "https://api.telegram.org" if "api_url" not in assets.keys() or assets["api_url"] == "" else assets["api_url"]
    Proxies = None
    if 'http_proxy' in assets.keys() and assets['http_proxy'] != '':
        http_proxy = assets['http_proxy']
        Proxies = {
            "http": http_proxy,
            "https": http_proxy
        }
    # 返回值
    json_ret = {"code": 500, "msg": "","data": {"success": False}}

    '''添加函数实现
    
    '''
    url = f'{api_url}/bot{bot_token}/getMe'
    try:
        response = requests.get(url, proxies=Proxies, timeout=30)
        if response.status_code == 200:
            json_res = response.json()
            if 'ok' in json_res.keys() and json_res['ok'] is True:
                json_ret['data']['success'] = True
                json_ret['code'] = 200
                json_ret['msg'] = "测试成功"
        else:
            json_ret['msg'] = response.text
    except Exception as e:
        json_ret['msg'] = str(e)
    return json_ret 

