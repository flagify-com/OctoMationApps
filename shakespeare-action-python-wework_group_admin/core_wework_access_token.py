#coding:utf-8
import requests
import json
import time


"""
根据corpid和corpsecret获取企业微信的access_token，同时支持缓存管理。
当access_token在有效期内，使用缓存access_token，而当access_token过期时，重新获取一次。
缓存文件文件存储在本程序的当前目录下，文件名为{appid}_access_token.json。
https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET
"""

def cache_access_token(appid,access_token, expires_in):
    # 缓存access_token到文件
    json_cache = {
        'access_token': access_token,
        'expires_in': expires_in,
        'cache_time': int(time.time())
    }
    try:
        with open(f'{appid}_access_token.json', 'w+') as f:
            f.write(json.dumps(json_cache, ensure_ascii=False))
            f.close()
    except Exception as e:
        print(e)


def get_cache_access_token(appid):
    # 读取缓存文件
    try:
        with open(f'{appid}_access_token.json', 'r') as f:
            json_cache = json.loads(f.read())
            f.close()
            if int(time.time()) - json_cache['cache_time'] < json_cache['expires_in']:
                return json_cache['access_token']
    except Exception as e:
        print(e)
    return None

def get_access_token(appid, corpid, corpsecret):
    # 获取access_token
    access_token = None
    json_access_token = {
        'appid': appid,
        'access_token': access_token,
        'errmsg': 'Unknown Error',
        'errcode': -1
    }
    # 尝试读取缓存
    access_token = get_cache_access_token(appid)
    if access_token:
        json_access_token['access_token'] = access_token
        json_access_token['errcode'] = 0
        json_access_token['errmsg'] = 'use cached access_token'
        return json_access_token
    # 重新获取access_token
    try:
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        params = {'corpid': corpid, 'corpsecret': corpsecret}
        response = requests.get(url, params=params)
        json_res = response.json()
        json_access_token['errcode'] = json_res['errcode']
        
        if json_res['errcode'] == 0:
            access_token = json_res['access_token']
            expires_in = json_res['expires_in']
            cache_access_token(appid, access_token, expires_in)

            json_access_token['access_token'] = access_token
            json_access_token['errmsg'] = json_res['errmsg']
    except Exception as e:
        json_access_token['errmsg'] = str(e)
    
    return json_access_token

if __name__ == '__main__':
    # pip install python-dotenv
    from dotenv import load_dotenv
    import os

    load_dotenv()
    appid = os.getenv('APPID')
    corpid = os.getenv('CORPID')
    corpsecret = os.getenv('CORPSECRET')
    json_access_token = get_access_token(appid, corpid, corpsecret)
    print(json_access_token)