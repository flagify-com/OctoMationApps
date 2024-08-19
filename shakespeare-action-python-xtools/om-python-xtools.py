# -*- coding: utf-8 -*-

import re
import datetime
import time
import hashlib
import hmac
import base64
import urllib.parse
import ipaddress
import random
import shelve
from difflib import SequenceMatcher
import os
from action_sdk_for_cache.action_cache_sdk import HoneyGuide

def str_concat(params, assets, context_info):
    """
    按顺序拼接多个字符串，如果提供拼接符，则在字符串中间插入拼接符。#2024-08-18
    :param params: 参数字典，包含以下参数：
        - str1: 字符串1
        - str2: 字符串2
        - str3: 字符串3，可选参数，默认为空
        - str4: 字符串4，可选参数，默认为空
        - str5: 字符串5，可选参数，默认为空
        - str5: 字符串6，可选参数，默认为空
        - concat_symbol: 拼接符，可选参数，默认为空
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_concated": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str1"] = params.get("str1", "")
    json_ret["data"]["str2"] = params.get("str2", "")
    json_ret["data"]["str3"] = params.get("str3", "")
    json_ret["data"]["str4"] = params.get("str4", "")
    json_ret["data"]["str5"] = params.get("str5", "")
    json_ret["data"]["str6"] = params.get("str6", "")
    json_ret["data"]["concat_symbol"] = params.get("concat_symbol", "")
    str_array = [
        json_ret["data"]["str1"], json_ret["data"]["str2"],
        json_ret["data"]["str3"], json_ret["data"]["str4"],
        json_ret["data"]["str5"], json_ret["data"]["str6"]
    ]
    
    concat_str = json_ret["data"]["concat_symbol"].join(str_array)
    json_ret["data"]["str_concated"] = concat_str

    return json_ret

def str_split(params, assets, context_info):
    """
    按指定分隔符拆分字符串，返回拆分后的字符串数组。#2024-08-18
    :param params: 参数字典，包含以下参数：
        - str_to_split: 待拆分的字符串
        - split_symbol: 分隔符，可选参数，默认为英文逗号
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_splitted": []
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str_to_split"] = params.get("str_to_split", "")
    json_ret["data"]["split_symbol"] = params.get("split_symbol", ",")
    str_splitted = json_ret["data"]["str_to_split"].split(json_ret["data"]["split_symbol"])
    json_ret["data"]["str_splitted"] = str_splitted

    return json_ret

def str_splitlines(params, assets, context_info):
    """
    按行拆分字符串，返回拆分后的字符串数组。#2024-08-18
    :param params: 参数字典，包含以下参数：
        - str_to_split: 待拆分的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_splitted": []
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str_to_split"] = params.get("str_to_split", "")
    str_splitted = json_ret["data"]["str_to_split"].splitlines()
    json_ret["data"]["str_splitted"] = str_splitted

    return json_ret

def str_replace(params, assets, context_info):
    """
    替换字符串中的指定内容。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str_original: 待替换的原始字符串
        - str_old: 被替换的字符串
        - str_new: 替换后的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_replaced": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str_original"] = params.get("str_original", "")
    str_old = params.get("str_old", "")
    str_new = params.get("str_new", "")
    str_replaced = json_ret["data"]["str_original"].replace(str_old, str_new)
    json_ret["data"]["str_replaced"] = str_replaced

    return json_ret

def str_length(params, assets, context_info):
    """
    计算字符串长度。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待计算的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_length": 0
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "")
    json_ret["data"]["str_length"] = len(json_ret["data"]["str"])

    return json_ret

def str_reverse(params, assets, context_info):
    """
    字符串反转。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待反转的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_reversed": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "")
    json_ret["data"]["str_reversed"] = json_ret["data"]["str"][::-1]

    return json_ret

def str_substring_with_index(params, assets, context_info):
    """
    截取字符串，根据start和end位置[开始，结束)。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str_original: 待截取的字符串    
        - start: 开始位置（会被保留）
        - end: 结束位置（不被保留）
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_substring": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    str_original = params.get("str_original", "")
    start = params.get("start", 0)
    end = params.get("end", 0)
    try:
        json_ret["data"]["start"] = int(start)
        json_ret["data"]["end"] = int(end)
    except Exception as e:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = str(e)
        return json_ret
    json_ret["data"]["str_substring"] = str_original[start:end]

    return json_ret

def str_substring_with_start_and_length(params, assets, context_info):
    """
    截取字符串，根据start和length位置。  # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str_original: 待截取的字符串    
        - start: 开始位置
        - length: 截取长度
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_substring": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    str_original = params.get("str_original", "")
    start = params.get("start", 0)
    length = params.get("length", 0)
    try:
        json_ret["data"]["start"] = int(start)
        json_ret["data"]["length"] = int(length)    
    except Exception as e:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = str(e)
        return json_ret
    json_ret["data"]["str"] = str_original
    json_ret["data"]["str_substring"] = str_original[start:start+length]
    
    return json_ret

def str_to_int(params, assets, context_info):
    """
    字符串转整数。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待转换的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_int": 0
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "0")
    try:
        json_ret["data"]["str_int"] = int(json_ret["data"]["str"])
    except Exception as e:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = str(e)
    return json_ret

def str_to_double(params, assets, context_info):
    """
    字符串转浮点数（应对Java中的Double）。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待转换的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_double": 0.0
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "0.0")
    try:
        json_ret["data"]["str_double"] = float(json_ret["data"]["str"])
    except Exception as e:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = str(e)

    return json_ret

def str_to_long(params, assets, context_info):
    """
    字符串转整型（应对Java中的Long）。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待转换的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_long": 0
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "0")
    try:
        json_ret["data"]["str_long"] = int(json_ret["data"]["str"])
    except Exception as e:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = str(e)

    return json_ret

def str_to_bool(params, assets, context_info):
    """
    字符串转布尔值。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待转换的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_bool": False
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "")
    if json_ret["data"]["str"].lower() in ["true", "1", "t", "y", "yes", "success"]:
        json_ret["data"]["str_bool"] = True
    elif json_ret["data"]["str"].lower() ["false", "0", "f", "n", "no", "failure"]:
        json_ret["data"]["str_bool"] = False
    else:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Invalid boolean string"

    return json_ret

def str_to_upper(params, assets, context_info):
    """
    字符串转大写。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待转换的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_upper": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "")
    json_ret["data"]["str_upper"] = json_ret["data"]["str"].upper()

    return json_ret

def str_to_lower(params, assets, context_info):
    """
    字符串转小写。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待转换的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_lower": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "")
    json_ret["data"]["str_lower"] = json_ret["data"]["str"].lower()

    return json_ret

def str_strip(params, assets, context_info):    
    """
    去除字符串两端的空格。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待处理的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_stripped": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str_original"] = params.get("str_original", "")
    strip_method = params.get("strip_method", "both").lower()
    strip_symbol = params.get("strip_symbol", "")
    if strip_symbol == "":
        strip_symbol = None
    if strip_method == "left":
        json_ret["data"]["str_stripped"] = json_ret["data"]["str_original"].lstrip(strip_symbol)
    elif strip_method == "right":
        json_ret["data"]["str_stripped"] = json_ret["data"]["str_original"].rstrip(strip_symbol)
    else:
        json_ret["data"]["str_stripped"] = json_ret["data"]["str_original"].strip(strip_symbol)
    return json_ret

def str_escape(params, assets, context_info):
    """
    转义字符串中的特殊字符。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待转义的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_escaped": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str_original"] = params.get("str_original", "")
    
    escape_string_array = params.get("escape_string_array", ['\\', '"'])

    def escape_string(input_string):
        # 定义需要转义的字符及其替换
        escape_map = {
            '\\': '\\\\',  # 反斜杠
            '\'': '\\\'',  # 单引号
            '\"': '\\\"',  # 双引号
            '\n': '\\n',   # 换行符
            '\t': '\\t',   # 制表符
        }
        
        # 使用 str.replace() 方法进行转义替换
        for char, replacement in escape_map.items():
            if char in escape_string_array:
                input_string = input_string.replace(char, replacement)
        
        return input_string

    json_ret["data"]["str_escaped"] = escape_string(json_ret["data"]["str_original"])

    return json_ret

def str_random_string(params, assets, context_info):
    """
    生成随机字符串。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - min_length: 字符串最小长度
        - max_length: 字符串最大长度
        - avaliable_chars: 字符串包含的字符集，默认包含数字、大小写字母
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_random": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }

    min_length = params.get("min_length", 1)
    max_length = params.get("min_length", 10)
    try:
        min_length = int(min_length)
        max_length = int(max_length)
    except Exception as e:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = str(e)
        return json_ret
    if min_length < 1 or max_length < 1:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Invalid length: length < 1"
        return json_ret
    if min_length > max_length:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Invalid length: min_length > max_length"
        return json_ret
    length = random.randint(min_length, max_length)
    avaliable_chars = params.get("avaliable_chars", "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    json_ret["data"]["str_random"] = ''.join(random.choice(avaliable_chars) for i in range(length))
    return json_ret

# def regex_match

def type_to_type(params, assets, context_info):
    """
    通用类型转换。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - input_value: 待转换的值
        - type_to: 目标类型
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "converted_value_int": 0,
            "converted_value_double": 0.0,
            "converted_value_long": 0,
            "converted_value_boolean": False,
            "converted_value_string": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    input_value = params.get("input_value", "")
    type_to = params.get("type_to", "string").lower()
    try:
        if type_to == "string" or type_to == "str":
            json_ret["data"]["converted_value_string"] = str(input_value)
        elif type_to == "integer" or type_to == "int":
            json_ret["data"]["converted_value_int"] = int(input_value)
        elif type_to == "double":
            json_ret["data"]["converted_value_double"] = float(input_value)
        elif type_to == "long":
            json_ret["data"]["converted_value_long"] = int(input_value)
        elif type_to == "boolean" or type_to == "bool":
            if input_value.lower() in ["true", "1", "t", "y", "yes", "success"]:
                json_ret["data"]["converted_value_boolean"] = True
            elif input_value.lower() in ["false", "0", "f", "n", "no", "failure"]:
                json_ret["data"]["converted_value_boolean"] = False
            else:
                json_ret["summary"]["statusCode"] = 400
                json_ret["summary"]["msg"] = "Invalid boolean string"
        else:
            json_ret["summary"]["statusCode"] = 400
            json_ret["summary"]["msg"] = "Invalid type_to"
    except Exception as e:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = str(e)

    return json_ret


def datetime_timestamp_to_timestr(params, assets, context_info):
    """
    时间戳转时间字符串。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - timestamp: 时间戳（秒）
        - format: 时间格式，默认%Y-%m-%d %H:%M:%S
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "datetime_str": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    timestamp = params.get("timestamp", time.localtime())
    try:
        timestamp = int(timestamp)
    except Exception as e:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = str(e)
        return json_ret
    format = params.get("format", "%Y-%m-%d %H:%M:%S")
    try:
        json_ret["data"]["datetime_str"]  = time.strftime(format, time.localtime(timestamp))
    except Exception as e:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = str(e)
    return json_ret

def encode_base64encode(params, assets, context_info):
    """
    字符串编码为base64。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待编码的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_base64_encode": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "")
    if json_ret["data"]["str"] == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Empty string"
        return json_ret
    encode = params.get("encode", "utf-8")
    json_ret["data"]["str_base64_encode"] = base64.b64encode(json_ret["data"]["str"].encode(encode)).decode(encode)
    return json_ret

def encode_base64decode(params, assets, context_info):
    """
    base64解码为字符串。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str_base64: 待解码的base64字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_base64_decode": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str_base64"] = params.get("str_base64", "")
    if json_ret["data"]["str_base64"] == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Empty base64 string"
        return json_ret
    decode = params.get("decode", "utf-8")
    json_ret["data"]["str_base64_decode"] = base64.b64decode(json_ret["data"]["str_base64"]).decode(decode)
    return json_ret

def encode_urlencode(params, assets, context_info):
    """
    字符串编码为url编码。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str: 待编码的字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_url_encoded": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "")
    if json_ret["data"]["str"] == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Empty string"
        return json_ret
    json_ret["data"]["str_url_encoded"] = urllib.parse.quote(json_ret["data"]["str"])
    return json_ret

def encode_urldecode(params, assets, context_info):
    """
    url解码为字符串。 # 2024-08-18
    :param params: 参数字典，包含以下参数：
        - str_url_encoded: 待解码的url encoded字符串
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_url_decoded": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str_url_encoded"] = params.get("str_url_encoded", "")
    if json_ret["data"]["str_url_encoded"] == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Empty url encoded string"
    json_ret["data"]["str_url_decoded"] = urllib.parse.unquote(json_ret["data"]["str_url_encoded"])
    return json_ret

def encrypt_hash(params, assets, context_info):
    """
    字符串加密为hash。 # 2024-08-19
    :param params: 参数字典，包含以下参数：
        - str: 待加密的字符串        
        - hash_method: 加密方法，默认md5
        - encode: 编码方式，默认utf-8
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_hashed": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "")
    encode = params.get("encode", "utf-8").lower()
    if encode == "":
        encode = "utf-8"
    if json_ret["data"]["str"] == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Empty string"
        return json_ret
    hash_method = params.get("hash_method", "md5").lower()
    if  hash_method == "md5":
        m = hashlib.md5()
    elif  hash_method == "sha1":
        m = hashlib.sha1()
    elif hash_method == "sha224":
        m = hashlib.sha224()
    elif hash_method == "sha256":
        m = hashlib.sha256()
    elif hash_method == "sha384":
        m = hashlib.sha256()
    elif hash_method == "sha512":
        m = hashlib.sha512()
    elif hash_method == "sha3_224":
        m = hashlib.sha3_224()
    elif hash_method == "sha3_256":
        m = hashlib.sha3_256()
    elif hash_method == "sha3_384":
        m = hashlib.sha3_384()
    elif hash_method == "sha3_512":
        m = hashlib.sha3_512()
    elif hash_method == "blake2b":
        m = hashlib.blake2b()
    elif hash_method == "blake2s":
        m = hashlib.blake2s()
    elif hash_method == "shake_128":
        m = hashlib.shake_128()
    elif hash_method == "shake_256":
        m = hashlib.shake_256()
    else:
        m = hashlib.md5()
    m.update(json_ret["data"]["str"].encode(encode))
    json_ret["data"]["str_hashed"] = m.hexdigest()
    return json_ret

def encrypt_hmac(params, assets, context_info):
    """
    字符串加密为hmac。 # 2024-08-19
    :param params: 参数字典，包含以下参数：
        - str: 待加密的字符串
        - key: 密钥
        - digest_method: 加密方法，默认sha256
        - encode: 编码方式，默认utf-8
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "str_hmaced": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    json_ret["data"]["str"] = params.get("str", "")
    encode = params.get("encode", "utf-8").lower()
    if encode == "":
        encode = "utf-8"
    if json_ret["data"]["str"] == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Empty string"
        return json_ret
    key = params.get("key", "")
    if key == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Empty key"
        return json_ret
    hash_method = params.get("hash_method", "md5").lower()
    if  hash_method == "md5":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.md5)
    elif hash_method == "sha1":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.sha1)
    elif hash_method == "sha224":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.sha224)
    elif hash_method == "sha256":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.sha256)
    elif hash_method == "sha384":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.sha384)
    elif hash_method == "sha512":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.sha512)
    elif hash_method == "sha3_224":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.sha3_224)
    elif hash_method == "sha3_256":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.sha3_256)
    elif hash_method == "sha3_384":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.sha3_384)
    elif hash_method == "sha3_512":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.sha3_512)
    elif hash_method == "blake2b":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.blake2b)
    elif hash_method == "blake2s":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.blake2s)
    elif hash_method == "shake_128":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.shake_128)
    elif hash_method == "shake_256":
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.shake_256)
    else:
        m = hmac.new(key.encode(encode), json_ret["data"]["str"].encode(encode), hashlib.md5)
    json_ret["data"]["str_hmaced"] = m.hexdigest()
    return json_ret

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def file_info(params, assets, context_info):
    """
    获取文件信息。 # 2024-08-19
    :param params: 参数字典，包含以下参数：
        - file_path: 文件路径
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "isdir": False,
            "isfile": False,
            "islink": False,
            "file_name": "",
            "file_realpath": "",
            "file_relativepath": "",
            "file_dirname": "",
            "file_size": 0,
            "file_ctime": 0,
            "file_ctime_str": "",
            "file_mtime": 0,
            "file_mtime_str": "",
            "file_atime": 0,
            "file_atime_str": "",
            "file_md5sum": "",
            "file_exists": True
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    file_path = params.get("file_path", "")
    json_ret["data"]["file_name"] = os.path.basename(file_path)
    json_ret["data"]["file_dirname"] = os.path.dirname(file_path)
    json_ret["data"]["file_realpath"] = os.path.realpath(file_path)
    json_ret["data"]["file_relativepath"] = os.path.relpath(file_path)

    if not os.path.exists(file_path):
        json_ret["data"]["file_exists"] = False
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "File or Path does not exist"
        return json_ret
    
    if os.path.isdir(file_path):
        json_ret["data"]["isdir"] = True
    elif os.path.isfile(file_path):
        json_ret["data"]["isfile"] = True
    elif os.path.islink(file_path):
        json_ret["data"]["islink"] = True

    if json_ret["data"]["isfile"]:
        try:
            json_ret["data"]["file_size"] = int(os.path.getsize(file_path))
            json_ret["data"]["file_ctime"] = int(os.path.getctime(file_path))
            json_ret["data"]["file_ctime_str"] = datetime.datetime.fromtimestamp(json_ret["data"]["file_ctime"]).strftime('%Y-%m-%d %H:%M:%S')
            json_ret["data"]["file_mtime"] = int(os.path.getmtime(file_path))
            json_ret["data"]["file_mtime_str"] = datetime.datetime.fromtimestamp(json_ret["data"]["file_mtime"]).strftime('%Y-%m-%d %H:%M:%S')
            json_ret["data"]["file_atime"] = int(os.path.getatime(file_path))
            json_ret["data"]["file_atime_str"] = datetime.datetime.fromtimestamp(json_ret["data"]["file_atime"]).strftime('%Y-%m-%d %H:%M:%S')
            with open(file_path, "rb") as f:
                json_ret["data"]["file_md5sum"] = hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            json_ret["summary"]["statusCode"] = 500
            json_ret["summary"]["msg"] = str(e)
    return json_ret



def file_read(params, assets, context_info):
    """
    读取文件内容。 # 2024-08-19
    :param params: 参数字典，包含以下参数：
        - file_path: 文件路径
        - encode: 编码方式，默认utf-8
        - file_size_limit: 文件大小限制，单位KB，默认512KB
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "file_content_text": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    file_path = params.get("file_path", "")
    if not os.path.exists(file_path):
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "File or Path does not exist"
        return json_ret
    
    encode = params.get("encode", "utf-8").lower()
    if encode == "":
        encode = "utf-8"
    file_size_limit = params.get("file_size_limit", 512)
    try:
        file_size_limit = int(file_size_limit)
    except Exception as e:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Invalid file_size_limit number"
        return json_ret
    
    # 判断文件大小是否超过限制
    if os.path.getsize(file_path) > file_size_limit * 1024:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "File size exceeds limit"
        return json_ret
    try:
        with open(file_path, "r", encoding=encode) as f:
            json_ret["data"]["file_content_text"] = f.read()
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = str(e)
    return json_ret

def int_to_str(params, assets, context_info):
    """
    整数转字符串。 # 2024-08-19
    :param params: 参数字典，包含以下参数：
        - int_data: 整数数据
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "int_str": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    int_data = params.get("int_data", 0)
    if not int_data:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Empty integer"
        return json_ret
    json_ret["data"]["int_str"] = str(int_data)
    return json_ret


def math_expression(params, assets, context_info):
    """
    数学计算，根据表达式返回结算结果 # 2024-08-19
    :param params: 参数字典，包含以下参数：
        - expression: 数学表达式，支持加减乘除、括号、常量、变量
    """
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "int_value": 0,
            "long_value": 0,
            "double_value": 0.0,
            "string_value": "0"
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }
    expression = params.get("expression", "1+1")
    if not expression:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Empty expression"
        return json_ret
    if 'import' in expression or 'eval' in expression:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Forbidden expression"
        return json_ret
    # 正则表达式，判断字符串为数学计算表达式，包含：加、减、乘、除、括号、取余、科学计数等...
    pattern = re.compile(r'^[-+*/()0-9.eE^%\s]+$')
    if not pattern.match(expression):
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "Invalid expression"
        return json_ret
    try:
        result = eval(expression)
        json_ret["data"]["int_value"] = int(result)
        json_ret["data"]["long_value"] = int(result)
        json_ret["data"]["double_value"] = float(result)
        json_ret["data"]["string_value"] = str(result)
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = str(e)
    return json_ret


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

    json_ret = {"code": 200, "msg": "", "data": {"key": _key, "value": "","status": False}}

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
            json_ret['data']["value"] = _value
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

def get_file_download_url(params, assets, context_info):
    # 获取文件路径
    json_ret = {
        "code": 200, 
        "msg": "",
        "data":{
            "download_url": "",
            "uuid": ""},
        "summary":{
            "statusCode":0,
            "msg": ""
        }}
    file_path = params.get('file_path', "")
    if not os.path.exists(file_path):
        json_ret["code"] = 400
        json_ret["msg"] = "File not found"
        return json_ret
    hg_client = HoneyGuide(context_info=context_info)
    file_uuid = hg_client.fileCache.save(file_path, keepDays=1)
    # hg_client.actionLog.info(f"File {file_path} is cached with uuid {file_uuid}")
    download_url = hg_client.fileCache.downloadUrl(file_uuid)
    json_ret['data']['uuid'] = file_uuid
    json_ret['data']['download_url'] = download_url
    return json_ret