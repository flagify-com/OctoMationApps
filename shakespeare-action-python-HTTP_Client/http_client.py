# -*- coding: utf-8 -*-
import requests
import time
import pickle
import os
from http.cookiejar import CookieJar

def from_cookiejar_to_string(cookiejar):
    """
    将CookieJar对象转换成Cookie字符串，用于HTTP HEADER
    """
    cookie_string = ''
    if isinstance(cookiejar, CookieJar):
        for cookie in cookiejar:
            cookie_string += f'{cookie.name}={cookie.value}; '
        # Remove the trailing semicolon and space
        cookie_string = cookie_string[:-2]
    return cookie_string

def save_cookie_to_pickle_file(cookies, cookie_file):
    """
    保存Cookie文件，暂时未做异常处理
    """
    if cookie_file != "":
        with open(cookie_file, 'wb+') as file:
            pickle.dump(cookies, file)
            file.close()

def read_cookie_to_pickle_file(cookie_file):
    """
    从文件中读取Cookie，暂时未做异常处理
    """
    cookies = None
    if os.path.exists(cookie_file):
        with open(cookie_file, 'rb') as file:
            print(cookies)
            cookies = pickle.load(file)
            file.close()
    return cookies
        

def http_request(params, assets, context_info):
    """HTTP请求"""

    # URL服务器，如：https://user:pass@example.com:8080
    SERVER = params["SERVER"]
    # URL路径，如：/user/info，默认为：/
    PATH = "/" if "PATH" not in params.keys() or params["PATH"] == "" else params["PATH"]
    # URL请求参数(不带?，需自行做好URL Encode，如：user=Chris&comment=I%20love%20OctoMation）
    QUERY = ""
    if "QUERY" in params.keys() and params["QUERY"] != "" and params["QUERY"] is not None: QUERY= params["QUERY"]
    # HTTP请求头中的User Agent，默认为：OctoMation-HTTP-Client v1.0.0
    USER_AGENT = "OctoMation-HTTP-Client v1.0.0" if "USER_AGENT" not in params.keys() or params["USER_AGENT"] == "" else params["USER_AGENT"]
    # HTTP请求头中的Content-Type，默认：application/json
    CONTENT_TYPE = "" if "CONTENT_TYPE" not in params.keys() or params["CONTENT_TYPE"] == "" else params["CONTENT_TYPE"]
    # 自定义HTTP头，KEY:VALUE，按行填写。
    HEADER = ""
    if "HEADER" in params.keys() and params["HEADER"] != "" and params["HEADER"] is not None: HEADER= params["HEADER"]
    # HTTP请求体（Form模式需要自行URL Encode）
    BODY = ""
    if "BODY" in params.keys() and params["BODY"] != "" and params["BODY"] is not None: BODY= params["BODY"]
    # HTTP请求方法，默认：GET
    METHOD = "GET" if "METHOD" not in params.keys() or params["METHOD"] == "" else params["METHOD"]

    COOKIE_FILE = ""
    if "COOKIE_FILE" in params.keys() and params["COOKIE_FILE"] != "" and params["COOKIE_FILE"] is not None:
        if '__RANDOM__COOKIE__FILE__' == params["COOKIE_FILE"]:
            # 随机一个Cookie文件名（Pickle格式的）
            cookie_file = int(time.time()*1000)
            COOKIE_FILE = f'/tmp/cookie.{cookie_file}.pkl'
        else:
            COOKIE_FILE =  params["COOKIE_FILE"]
        # 初始化一个存放Cookie的文件
        if not os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, 'wb+') as file:
                pickle.dump(None, file)
                file.close()

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
    json_ret = {"code": 200, "msg": "","data": {"http_response_code": 0, "http_response_text": "", "cookies":"", "cookie_file": COOKIE_FILE}}

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
    if USER_AGENT != "":
        headers['user-agent'] = USER_AGENT
    for headline in HEADER.split("\n"):
        if ':' in headline:
            key = headline.split(':')[0].strip()
            value = headline.split(':')[-1].strip()
            if key != "" and value != "":
                headers[key.lower()] = value.lower()
    
    try:
        cookies = read_cookie_to_pickle_file(COOKIE_FILE)
        s = requests.session()
        if cookies:
            s.cookies = cookies
        res = None
        if 'GET'  == METHOD:
            res = s.get(url=url, headers=headers, allow_redirects=ALLOW_REDIRECTS, proxies=PROXY, verify=VERIFY_SSL, timeout=TIMEOUT)
        elif 'HEAD'  == METHOD:
            res = s.head(url=url, headers=headers, allow_redirects=ALLOW_REDIRECTS, proxies=PROXY, verify=VERIFY_SSL, timeout=TIMEOUT)
        elif 'DELETE'  == METHOD:
            res = s.delete(url=url, headers=headers, allow_redirects=ALLOW_REDIRECTS, proxies=PROXY, verify=VERIFY_SSL, timeout=TIMEOUT)
        elif 'OPTIONS'  == METHOD:
            res = s.options(url=url, headers=headers, allow_redirects=ALLOW_REDIRECTS, proxies=PROXY, verify=VERIFY_SSL, timeout=TIMEOUT)
        elif 'POST' == METHOD:
            res = s.post(url=url, headers=headers, data=BODY.encode(), allow_redirects=ALLOW_REDIRECTS,proxies=PROXY, verify=VERIFY_SSL, timeout=TIMEOUT)
        elif 'PUT' == METHOD:
            res = s.put(url=url, headers=headers, data=BODY.encode(), allow_redirects=ALLOW_REDIRECTS,proxies=PROXY, verify=VERIFY_SSL, timeout=TIMEOUT)
        if res is not None:
            save_cookie_to_pickle_file(s.cookies, COOKIE_FILE)
            json_ret['data']['http_response_code'] = res.status_code
            json_ret['data']['http_response_text'] = res.text
            json_ret['data']['cookies'] = from_cookiejar_to_string(s.cookies)
        if json_ret['data']['http_response_code'] in (200, 201):
            json_ret['msg'] = "请求发送成功，请确认返回结果:)"
        else:
            json_ret['msg'] = "可能请求失败，请检查错误信息:("
    except Exception as e:
        json_ret['code']= 500
        json_ret["msg"] = str(e)

    return json_ret
