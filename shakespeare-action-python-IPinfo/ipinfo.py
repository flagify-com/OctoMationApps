# -*- coding: utf-8 -*-
import requests
import json

def get_ip_geolocation(params, assets, context_info):
    """查询IP地址的地理位置"""

    # API Token
    token = assets["token"]
    # IP地址（支持IPv4、IPv6）
    ip = "8.8.8.8" if "ip" not in params.keys() or params["ip"] == "" else params["ip"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"ip": "", "city": "", "region": "", "country": "", "loc": "", "org": "", "timezone": "", "postal": ""}}

    '''添加函数实现
    
    '''
    url = f"https://ipinfo.io/{ip}?dataset=geolocation&token={token}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_info = response.json()
            if 'ip' in json_info.keys():
                json_ret['data']['ip'] = json_info['ip']
            if 'city' in json_info.keys():
                json_ret['data']['city'] = json_info['city']
            if 'region' in json_info.keys():
                json_ret['data']['region'] = json_info['region']
            if 'country' in json_info.keys():
                json_ret['data']['country'] = json_info['country']
            if 'loc' in json_info.keys():
                json_ret['data']['loc'] = json_info['loc']
            if 'org' in json_info.keys():
                json_ret['data']['org'] = json_info['org']
            if 'postal' in json_info.keys():
                json_ret['data']['postal'] = json_info['postal']
            if 'timezone' in json_info.keys():
                json_ret['data']['postal'] = json_info['timezone']
    except Exception as e:
        json_ret['msg'] = str(e)

    return json_ret 
