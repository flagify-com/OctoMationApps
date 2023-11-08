# -*- coding: utf-8 -*-
import requests
import time
import os
import json
from urllib.parse import urlparse
from http.cookiejar import Cookie, CookieJar, MozillaCookieJar

def save_cookie_to_file(obj_cookie_jar, cookie_file):
    """
    将CookieJar对象转换为MozillaCookieJar，并存储到文件
    """
    mozilla_cookiejar = MozillaCookieJar()
    for cookie in obj_cookie_jar:
        mozilla_cookiejar.set_cookie(cookie)
    mozilla_cookiejar.save(cookie_file, ignore_discard=True, ignore_expires=True)

def load_cookie_from_file(cookie_file):
    """
    从文件加载MozillaCookieJar对象，并转换成CookieJar对象
    """
    cookiejar = CookieJar()
    if os.path.exists(cookie_file):
        mozilla_cookiejar = MozillaCookieJar()
        try:
            mozilla_cookiejar.load(cookie_file, ignore_discard=True, ignore_expires=True)
            for cookie in mozilla_cookiejar:
                cookiejar.set_cookie(cookie)
        except Exception as e:
            print(e)
    return cookiejar

def from_string_to_cookiejar(cookie_string, domain):
    """
    将Cookie字符串转换为CookieJar对象，如："vk=70acfa88; cbc-sid=20493701 "
    """
    cookie_jar = CookieJar()
    for item in cookie_string.split(';'):
        name, value = item.strip().split('=', 1)
        cookie = Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain=domain,
            domain_specified=False,
            domain_initial_dot=False,
            path='/',
            path_specified=True,
            secure=False,
            expires=None,
            discard=True,
            comment=None,
            comment_url=None,
            rest={'HttpOnly': None},
            rfc2109=False,
        )
        cookie_jar.set_cookie(cookie)
    return cookie_jar

def from_cookiejar_to_string(cookiejar):
    """
    将CookieJar对象转换成Cookie字符串，用于HTTP请求中的HEAD
    """
    cookie_string = ''
    if isinstance(cookiejar, CookieJar):
        for cookie in cookiejar:
            cookie_string += f'{cookie.name}={cookie.value}; '
        # Remove the trailing semicolon and space
        cookie_string = cookie_string[:-2]
    return cookie_string

def http_request(params, assets, context_info):
    """通用HTTP请求"""

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

    COOKIES = ""
    if "COOKIES" in params.keys() and params["COOKIES"] != "" and params["COOKIES"] is not None: COOKIES= params["COOKIES"]

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
            save_cookie_to_file(CookieJar(), COOKIE_FILE)

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
    json_ret = {
        "code": 200, 
        "msg": "",
        "data": {
            "http_response_code": 0, 
            "http_response_text": "", 
            "http_response_headers": {}, 
            "cookies": COOKIES, 
            "cookie_file": COOKIE_FILE
        }
    }

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
        cookies_for_request = None
        # COOKIES字符串存在的情况下，优先使用COOKIES
        if COOKIES != "":
            domain = urlparse(url).hostname
            cookies_for_request = from_string_to_cookiejar(COOKIES, domain)
        elif COOKIE_FILE != "":
            cookies_for_request = load_cookie_from_file(COOKIE_FILE)
        else:
            cookies_for_request = CookieJar()

        s = requests.session()
        if cookies_for_request:
            s.cookies = cookies_for_request

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
            for cookie in s.cookies:
                cookies_for_request.set_cookie(cookie)
            if COOKIE_FILE != "":
                save_cookie_to_file(cookies_for_request, COOKIE_FILE)
            json_ret['data']['http_response_code'] = res.status_code
            json_ret['data']['http_response_text'] = res.text
            json_ret['data']['http_response_headers'] =json.loads(json.dumps(dict(res.headers)))
            json_ret['data']['cookies'] = from_cookiejar_to_string(cookies_for_request)

        if json_ret['data']['http_response_code'] in (200, 201):
            json_ret['msg'] = "请求发送成功，请确认返回结果:)"
        else:
            json_ret['msg'] = "可能请求失败，请检查错误信息:("
    except Exception as e:
        json_ret['code']= 500
        json_ret["msg"] = str(e)

    return json_ret