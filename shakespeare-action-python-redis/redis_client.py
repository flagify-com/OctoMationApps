# -*- coding: utf-8 -*-
import redis

def health_check(params, assets, context_info):
    """health_check"""

    host = assets.get("host")
    port = int(assets.get("port", 6379))
    db = int(assets.get("db", 0))
    password = assets.get("password", None)
    socket_timeout_seconds = int(assets.get("socket_timeout_seconds", 0))
    
    if socket_timeout_seconds == 0:
        socket_timeout_seconds = None

    json_ret = {"code": 200, "msg": "","data": {"success": False}, "summary": {"statusCode":200, "msg": ""}}
    
    try:
        r = redis.Redis(host, port, db, password,socket_timeout_seconds)
        if r.set("honeyguide_soar_health_check", "wuzhizhineng"):
            json_ret['data']['success'] = True
            json_ret["summary"]["statusCode"] = 200
            json_ret['summary']['msg'] = "健康性检查成功:)"
        else:
            json_ret["summary"]["statusCode"] = 500
            json_ret['summary']['msg'] = "健康性检查失败:("
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = "{0}:{1}".format(type(e), str(e))
        json_ret['msg'] = "健康性检查失败:("

    return json_ret

def redis_get(params, assets, context_info):
    """GET"""

    host = assets.get("host")
    port = int(assets.get("port", 6379))
    db = int(assets.get("db", 0))
    password = assets.get("password", None)
    encode = assets.get("encode", 'utf-8')
    socket_timeout_seconds = int(assets.get("socket_timeout_seconds", 0))
    
    if socket_timeout_seconds == 0:
        socket_timeout_seconds = None

    key = params["key"]

    json_ret = {"code": 200, "msg": "","data": {"key": key, "value": ""}, "summary": {"statusCode":200, "msg": ""}}
    
    try:
        r = redis.Redis(host, port, db, password,socket_timeout_seconds)
        value = r.get(key)
        if value is None:
            json_ret["summary"]["msg"] = "No result"
        else:
            json_ret["data"]["value"] = value.decode(encode)
            json_ret["summary"]["msg"] = "operation success"
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = "{0}:{1}".format(type(e), str(e))
        json_ret["msg"] = str(e)
    return json_ret

def redis_set(params, assets, context_info):
    """SET"""

    host = assets.get("host")
    port = int(assets.get("port", 6379))
    db = int(assets.get("db", 0))
    password = assets.get("password", None)
    socket_timeout_seconds = int(assets.get("socket_timeout_seconds", 0))
    
    if socket_timeout_seconds == 0:
        socket_timeout_seconds = None

    key = params["key"]
    value = params["value"]
    expire_seconds = int(assets.get("expire_seconds", 0))

    json_ret = {"code": 200, "msg": "","data": {"key": key, "success": False}, "summary": {"statusCode":200, "msg": ""}}
    
    try:
        r = redis.Redis(host, port, db, password,socket_timeout_seconds)
        if r.set(key, value):
            if expire_seconds > 0:
                r.expire(key,expire_seconds)
            json_ret["data"]["success"] = True
            json_ret["summary"]["msg"] = "operation success"
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = "{0}:{1}".format(type(e), str(e))
        json_ret["msg"] = str(e)

    return json_ret

def redis_lpush(params, assets, context_info):
    """LPUSH"""

    host = assets.get("host")
    port = int(assets.get("port", 6379))
    db = int(assets.get("db", 0))
    password = assets.get("password", None)
    socket_timeout_seconds = int(assets.get("socket_timeout_seconds", 0))
    
    if socket_timeout_seconds == 0:
        socket_timeout_seconds = None

    key = params["key"]
    value = params["value"]

    json_ret = {"code": 200, "msg": "","data": {"key": key, "success": False, "length": 0}, "summary": {"statusCode":200, "msg": ""}}
    
    try:
        r = redis.Redis(host, port, db, password,socket_timeout_seconds)
        length =  r.lpush(key, value)
        if length >= 0:
            json_ret["data"]["success"] = True
            json_ret["data"]["length"] = length
            json_ret["summary"]["msg"] = "operation success"
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = "{0}:{1}".format(type(e), str(e))
        json_ret["msg"] = str(e)

    return json_ret 

def redis_rpop(params, assets, context_info):
    """RPOP"""

    host = assets.get("host")
    port = int(assets.get("port", 6379))
    db = int(assets.get("db", 0))
    password = assets.get("password", None)
    encode = assets.get("encode", 'utf-8')
    socket_timeout_seconds = int(assets.get("socket_timeout_seconds", 0))
    
    if socket_timeout_seconds == 0:
        socket_timeout_seconds = None

    key = params["key"]

    json_ret = {"code": 200, "msg": "","data": {"key": key, "value": ""}, "summary": {"statusCode":200, "msg": ""}}
    
    try:
        r = redis.Redis(host, port, db, password,socket_timeout_seconds)
        value =  r.rpop(key)
        if value is None:
            json_ret["summary"]["msg"] = "No result"
        else:
            json_ret["data"]["value"] = value.decode(encode)
            json_ret["summary"]["msg"] = "operation success"
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = "{0}:{1}".format(type(e), str(e))
        json_ret["msg"] = str(e)


    return json_ret 

def redis_exists(params, assets, context_info):
    """EXISTS"""

    host = assets.get("host")
    port = int(assets.get("port", 6379))
    db = int(assets.get("db", 0))
    password = assets.get("password", None)
    socket_timeout_seconds = int(assets.get("socket_timeout_seconds", 0))
    
    if socket_timeout_seconds == 0:
        socket_timeout_seconds = None

    key = params["key"]

    json_ret = {"code": 200, "msg": "","data": {"key": key, "exists": False}, "summary": {"statusCode":200, "msg": ""}}
    
    try:
        r = redis.Redis(host, port, db, password,socket_timeout_seconds)
        exists =  r.exists(key)
        if exists:
            json_ret["data"]["exists"] = True
            json_ret["msg"] = "Key存在:)"
        else:
            json_ret["msg"] = "Key不存在:("
        json_ret["summary"]["msg"] = "operation success"
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = "{0}:{1}".format(type(e), str(e))
        json_ret["msg"] = str(e)

    return json_ret 

def redis_del(params, assets, context_info):
    """DEL"""

    host = assets.get("host")
    port = int(assets.get("port", 6379))
    db = int(assets.get("db", 0))
    password = assets.get("password", None)
    encode = assets.get("encode", 'utf-8')
    socket_timeout_seconds = int(assets.get("socket_timeout_seconds", 0))
    
    if socket_timeout_seconds == 0:
        socket_timeout_seconds = None

    key = params["key"]

    json_ret = {"code": 200, "msg": "","data": {"key": key, "success": False}, "summary": {"statusCode":200, "msg": ""}}
    
    try:
        r = redis.Redis(host, port, db, password,socket_timeout_seconds)
        if r.delete(key):
            json_ret["data"]["success"] = True
            json_ret["summary"]["msg"] = "operation success"
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = "{0}:{1}".format(type(e), str(e))
        json_ret["msg"] = str(e)

    return json_ret 

def redis_llen(params, assets, context_info):
    """LLEN"""

    host = assets.get("host")
    port = int(assets.get("port", 6379))
    db = int(assets.get("db", 0))
    password = assets.get("password", None)
    socket_timeout_seconds = int(assets.get("socket_timeout_seconds", 0))
    
    if socket_timeout_seconds == 0:
        socket_timeout_seconds = None

    key = params["key"]

    json_ret = {"code": 200, "msg": "","data": {"key": key, "length": 0}, "summary": {"statusCode":200, "msg": ""}}
    
    try:
        r = redis.Redis(host, port, db, password,socket_timeout_seconds)
        len = r.llen(key)
        if len:
            json_ret["data"]["length"] = len
            json_ret["summary"]["msg"] = "operation success"
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = "{0}:{1}".format(type(e), str(e))
        json_ret["msg"] = str(e)

    return json_ret 

def redis_raw_command(params, assets, context_info):
    """执行原始命令"""

    host = assets.get("host")
    port = int(assets.get("port", 6379))
    db = int(assets.get("db", 0))
    password = assets.get("password", None)
    socket_timeout_seconds = int(assets.get("socket_timeout_seconds", 0))
    
    if socket_timeout_seconds == 0:
        socket_timeout_seconds = None

    command = params["command"]

    json_ret = {"code": 200, "msg": "","data": {"command": command, "value": ""}, "summary": {"statusCode":200, "msg": ""}}
    
    try:
        r = redis.Redis(host, port, db, password,socket_timeout_seconds)
        parts = command.split()
        result = r.execute_command(*parts)
        json_ret["data"]["value"] = result
        json_ret["summary"]["msg"] = "Redis命令执行成功"
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = "{0}:{1}".format(type(e), str(e))
        json_ret["msg"] = str(e)


    return json_ret 


if __name__ == '__main__':
    assets = {
        "host": "192.168.44.2",
        "password": "qwe123"
    }
    params = {
        "key": "honeyguide_redis_test",
        "value": "ddd"
    }
    params_lpush = {
        "key": "honeyguide_redis_lpush_test",
        "value": "ddd"
    }
    params_command = {
        "key": "honeyguide_redis_lpush_test",
        "command": "lrange honeyguide_redis_lpush_test 0 3"
    }
