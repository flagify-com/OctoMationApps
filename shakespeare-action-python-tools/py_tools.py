# -*- coding: utf-8 -*-

import re
import datetime
import hashlib
import base64
import ipaddress
import shelve
from difflib import SequenceMatcher
import os


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


# 判断ip地址是否在某个段内
def ip_in_range(params, assets, context_info):
    #def ip_in_range(ip, start, end):
    ip = params.get('ip', "")
    start = params.get('start', "")
    end = params.get('end',"")

    json_ret = {"code": 200, "msg": "","data":{"is_range": False}}

    invalid_ips = [addr for addr in [ip, start, end] if not is_valid_ip(addr)]

    if invalid_ips:
        json_ret['code'] = 400
        json_ret['msg'] = f'Invalid IP format for: {", ".join(invalid_ips)}'
        return json_ret

    ip = ipaddress.ip_address(ip)
    start = ipaddress.ip_address(start)
    end = ipaddress.ip_address(end)

    json_ret['data']['is_range'] = ip >= start and ip <= end
    return json_ret

# 文本相似度
def str_similar(params, assets, context_info):
    s1 = params.get("one", "")
    s2 = params.get("two", "")
    #def str_similar(s1, s2):
    json_ret = {"code": 200, "msg": "","data":{"ratio": 0}}
    json_ret['data']['ratio'] = SequenceMatcher(None, s1, s2).ratio()
    return json_ret

# 时间比较（时间簇）
def date_comp(params, assets, context_info):
    date1 = params.get("one", 0)
    date2 = params.get("two", 0)

    json_ret = {"code": 200, "msg": "","data":{"result": 0}}
    #def date_comp(date1, date2):
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%d')
    if d1 > d2:
        json_ret['data']['result'] = 1
    elif d1 < d2:
        json_ret['data']['result'] = -1
    
    return json_ret

# 加法
def add(params, assets, context_info):
    a = params.get("one", 0)
    b = params.get("two", 0)
    #def add(a, b):
    json_ret = {"code": 200, "msg": "","data":{"result": a + b}}
    return json_ret

# 减法
def subtract(params, assets, context_info):
    #def subtract(a, b):
    a = params.get("one", 0)
    b = params.get("two", 0)
    json_ret = {"code": 200, "msg": "","data":{"result": a - b}}
    return json_ret

# 乘法
def multiply(params, assets, context_info):
    #def multiply(a, b):
    a = params.get("one", 0)
    b = params.get("two", 0)
    json_ret = {"code": 200, "msg": "","data":{"result": a * b}}

    return json_ret

# 除法
def divide(params, assets, context_info):
    #def divide(a, b):
    a = params.get("one", 0)
    b = params.get("two", 0)
    json_ret = {"code": 200, "msg": "","data":{"result": 0}}
    
    if b == 0:
        json_ret['code'] = 400
        json_ret['msg'] = "Divisor can't be 0"
        return json_ret
    
    try:
        json_ret['data']["result"] = a / b
    except Exception as e:
        json_ret['code'] = 500
        json_ret['msg'] = str(e)

    return json_ret

# 字符串输出
def input_output(params, assets, context_info):
    str_data = params.get("str_data","")
    out_type = params.get("out_type","str")

    json_ret = {"code": 200, "msg": "","data":{"str": "", "int": 0, "float": 0.0}}
    #def str_to_int(s):
    if out_type == "str":
        json_ret['data']['str'] = str_data
    elif out_type == "int":
        _int = 0
        try:
            _int = int(str_data)
            json_ret['data']['int'] = _int
        except Exception as e:
            json_ret['code'] = 500
            json_ret['msg'] = str(e)

    elif out_type == "float":
        _float = 0.0
        try:
            _float = float(str_data)
            json_ret['data']['float'] = _float
        except Exception as e:
            json_ret['code'] = 500
            json_ret['msg'] = str(e)

    return json_ret

# 整型转字符串
def int_to_str(params, assets, context_info):
    #def int_to_str(i):
    int_data = params.get("int_data",0)
    json_ret = {"code": 200, "msg": "","data":{"str": str(int_data)}}
    return json_ret

# 浮点型转字符串
def float_to_str(params, assets, context_info):
    float_data = params.get("float_data",0)
    json_ret = {"code": 200, "msg": "","data":{"str": str(float_data)}}
    #def float_to_str(f):
    return json_ret

# 字符串搜索
def search(params, assets, context_info):
    str_data = params.get("str_data","")
    sub = params.get("sub","")
    #def search(s, sub):
    json_ret = {"code": 200, "msg": "","data":{"is_find": str_data.find(sub) != -1}}
    return json_ret

# 正则匹配
def regex_match(params, assets, context_info):
    #def regex_match(s, pattern):
    str_data = params.get("str_data","")
    pattern = params.get("pattern","")
    json_ret = {"code": 200, "msg": "","data":{"findall": re.findall(pattern, str_data)}}
    return json_ret

# 计算md5
def md5(params, assets, context_info):
    s = params.get('str_data', "")
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    json_ret = {"code": 200, "msg": "","data":{"md5": m.hexdigest()}}
    return json_ret

# b64 en
def base64_encode(params, assets, context_info):
    s = params.get('str_data', "")
    json_ret = {"code": 200, "msg": "","data":{"b64": base64.b64encode(s.encode('utf-8')).decode('utf-8')}}
    return json_ret

# b64 de
def base64_decode(params, assets, context_info):
    s = params.get('b64_data', "")
    json_ret = {"code": 200, "msg": "","data":{"str": base64.b64decode(s).decode('utf-8')}}
    return json_ret   

# 字符串切割
def split(params, assets, context_info):
    s = params.get('str_data', "")
    sep = params.get('sep', "")
    json_ret = {"code": 200, "msg": "","data":{"str_list": []}}
    if s.find(sep) > -1:
        json_ret['data']['str_list'] = s.split(sep)
    return json_ret

# 字符串链接
def join(params, assets, context_info):
    str1 = params.get('one', "")
    str2 = params.get('two', "")
    json_ret = {"code": 200, "msg": "","data":{"str_data": f"{str1}{str2}"}}
    return json_ret

# 读取文件
def read_file(params, assets, context_info):
    filename = params.get("filename","")
    json_ret = {"code": 200, "msg": "","data":{"str_data": ""}}
    
    # 获取文件大小（以字节为单位）
    file_size_bytes = os.path.getsize(filename)

    # 定义0.5MB的字节数
    half_megabyte = 0.5 * 1024 * 1024  # 1 MB = 1024 KB, 1 KB = 1024 bytes

    # 检查文件大小是否小于0.5MB
    if file_size_bytes < half_megabyte:
        # 读取文件内容
        with open(filename, 'r', encoding='utf-8') as f:
            json_ret["data"]["str_data"] = f.read()
    else:
        json_ret["data"]["msg"] = "The file is 0.5MB or larger."     
        json_ret["code"] = 400
    return json_ret

# 字符串替换
def replace(params, assets, context_info):
    str_data = params.get('str_data', "")
    old_str = params.get('old_str',"")
    new_str = params.get('new_str',"")
    json_ret = {"code": 200, "msg": "","data":{"str_data": str_data.replace(old_str, new_str)}}
    return json_ret

# 时间字符串转时间簇
def date_to_timestamp(params, assets, context_info):
    date = params.get("date", "")
    json_ret = {"code": 200, "msg": "","data":{"timestamp": 0}}
    try:
        _t = int(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp())
        json_ret['data']['timestamp'] = _t
    except Exception as e:
        json_ret['code'] = 500
        json_ret['msg'] = str(e)
    return json_ret

# 时间簇转时间字符串
def timestamp_to_date(params, assets, context_info):
    timestamp = params.get("timestamp", 0)
    json_ret = {"code": 200, "msg": "","data":{"date": ""}}
    try:
        _d = str(datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
        json_ret['data']['date'] = _d
    except Exception as e:
        json_ret['code'] = 500
        json_ret['msg'] = str(e)

    return json_ret

# 字符串长度
def str_len(params, assets, context_info):
    str_data = params.get("srt_data", "")
    json_ret = {"code": 200, "msg": "","data":{"str_len": len(str_data)}}
    return json_ret



# 缓存管理
# def cache_mgmt(params, assets, context_info):
#     _key = params.get('key', "")
#     _value = params.get('value',None)
#     _ttl = params.get("tll",0)
#     _operate = params.get("operate", "get")

#     json_ret = {"code": 200, "msg": "","key": _key, "value": "", "status": False}
#     def open_cache(filename):
#         if not os.path.exists(filename):
#             db = shelve.open(filename) 
#             db.close()
#         return shelve.open(filename)

#     cache_file = open_cache("/tmp/cache_file")
#     if _operate == "get":
#         if key in cache_file:
#             value, expiration = cache_file[key]
#             if expiration is None or datetime.datetime.now() < expiration:
#                 json_ret['value'] = value
#                 json_ret['status'] = True
#     elif _options == "set":
#         if _ttl is None:
#             expiration = None
#         else:
#             expiration = datetime.datetime.now() + datetime.timedelta(seconds=_ttl)
#         cache_file[key] = (value, expiration)
#         json_ret['value'] = value
#         json_ret['status'] = True

#     elif _options == "del":
#         if key in cache_file:
#             del cache_file[key]
#             json_ret['value'] = value
#             json_ret['status'] = True

#     return json_ret


import diskcache as dc
def cache_mgmt(params, assets, context_info):
    # 创建一个缓存对象
    
    # 获取参数
    _key = params.get('key', "")
    _value = params.get('value', "")
    _ttl = params.get("ttl", None)
    _operate = params.get("operate", "get")

    json_ret = {"code": 200, "msg": "", "data": {"key": _key, "value": "", "status": False}}

    try:
        cache = dc.Cache("/opt/shakespeare/data/diskcache")

        if _operate == "get":
            # 尝试从缓存中获取值
            cached_value = cache.get(_key)
            if cached_value is not None:
                json_ret['data']["value"] = cached_value
                json_ret['data']["status"] = True
            else:
                # 如果缓存中没有该键，可以执行相应的操作，然后将结果存入缓存
                json_ret['data']["status"] = True

        elif _operate == "set":
            # 将值设置到缓存中
            cache.add(_key, _value, expire=_ttl)
            json_ret['data']["status"] = True
        elif _operate == "del":
            # 删除缓存中的键
            cache.pop(_key)
            json_ret['data']['status'] = True
        else:
            pass
            # 其他操作，根据需求自行添加
    except Exception as e:
        json_ret["code"] = 400
        json_ret["msg"] = str(e)
    finally:
        # 关闭缓存对象
        cache.close()

    return json_ret