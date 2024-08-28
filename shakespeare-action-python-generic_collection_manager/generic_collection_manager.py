# -*- coding: utf-8 -*-
from hg_api import HoneyGuideAPI
import re

def list_generic_collections(params, assets, context_info):
    # 获取所有集合，并返回集合组成的列表
    json_ret = {
        "code": 200, 
        "msg": "", 
        "data": {
            "collections": [],
            "count": 0
        }, 
        "summary": {
            "statusCode": 0, 
            "msg": ""
        }
    }
    hg_host = assets["hg_host"].strip().strip("/")
    hg_token = assets["hg_token"].strip()
    timeout_seconds = assets.get("timeout_seconds", 10)
    hg_api = HoneyGuideAPI(hg_host, hg_token, context_info=context_info, timeout_seconds=timeout_seconds)
    batch_size = params.get("batch_size", 30)
    max_count = params.get("max_count", 2000)
    try:
        batch_size = int(batch_size)
        max_count = int(max_count)
    except:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "batch_size和max_count必须为正整数"
        return json_ret
    collection_list = hg_api.get_generic_collections(batch_size=batch_size, max_count=max_count)
    json_ret["summary"]["statusCode"] = hg_api.summary["statusCode"]
    json_ret["summary"]["msg"] = hg_api.summary["msg"]
    if hg_api.summary["statusCode"] == 0:
        json_ret["data"]["collections"] = collection_list
        json_ret["data"]["count"] = len(collection_list)
    return json_ret

def create_generic_collection(params, assets, context_info):
    # 创建通用集合
    json_ret = {
        "code": 200, 
        "msg": "", 
        "data": {
            "collection_id": 0,
            "duplicated": False
        }, 
        "summary": {
            "statusCode": 0, 
            "msg": ""
        }
    }
    hg_host = assets["hg_host"].strip().strip("/")
    hg_token = assets["hg_token"].strip()
    timeout_seconds = assets.get("timeout_seconds", 10)
    hg_api = HoneyGuideAPI(hg_host, hg_token, context_info=context_info, timeout_seconds=timeout_seconds)
    collection_name = params["collection_name"].strip()
    collection_cnname = params["collection_cnname"].strip()
    collection_description = params.get("collection_description", "").strip()
    # collection_name只能包含数字，英文字母，下划线，需要正则匹配，不符合条件则返回错误
    if not re.match("^[a-zA-Z0-9_]+$", collection_name):
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "集合名称只能包含数字，英文字母，下划线,最长64字符"
        return json_ret
    if collection_cnname == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "集合中文名称不能为空"
        return json_ret

    # 创建集合
    collection_id = hg_api.create_generic_collection(collection_name, collection_cnname, collection_description)
    json_ret["summary"]["statusCode"]  = hg_api.summary["statusCode"]
    json_ret["summary"]["msg"] = hg_api.summary["msg"]
    json_ret["data"]["duplicated"] = hg_api.summary["duplicated"]
    if collection_id > 0:
        json_ret["data"]["collection_id"] = collection_id
    
    return json_ret

def delete_generic_collection(params, assets, context_info):
    # 删除通用集合
    json_ret = {
        "code": 200, 
        "msg": "", 
        "data": {}, 
        "summary": {
            "statusCode": -1, 
            "msg": ""
        }
    }
        
    collection_id = params.get("collection_id", 0)
    collection_name = params.get("collection_name", "")
    if collection_id == 0 and collection_name == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "collection_id和collection_name不能同时为空"
        return json_ret
    hg_host = assets["hg_host"].strip().strip("/")
    hg_token = assets["hg_token"].strip()
    timeout_seconds = assets.get("timeout_seconds", 10)
    hg_api = HoneyGuideAPI(hg_host, hg_token, context_info=context_info, timeout_seconds=timeout_seconds)
    if collection_id > 0:
        delete_result = hg_api.delete_generic_collection_by_id(collection_id)
    else:
        delete_result = hg_api.delete_generic_collection_by_name(collection_name)
    json_ret["summary"]["msg"] = hg_api.summary["msg"]
    json_ret["summary"]["statusCode"] = hg_api.summary["statusCode"]
    if delete_result:
        json_ret["summary"]["statusCode"] = 0
    return json_ret

def list_generic_collection_elements(params, assets, context_info):
    # 获取通用集合下的所有条目
    json_ret = {
        "code": 200, 
        "msg": "", 
        "data": {
            "elements": [],
            "count": 0
        }, 
        "summary": {
            "statusCode": 0, 
            "msg": ""
        }
    }

    hg_host = assets["hg_host"].strip().strip("/")
    hg_token = assets["hg_token"].strip()
    batch_size = params.get("batch_size", 30)
    max_count = params.get("max_count", 2000)
    try:
        batch_size = int(batch_size)
        max_count = int(max_count)
    except:
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "batch_size和max_count必须为正整数"
        return json_ret
    timeout_seconds = assets.get("timeout_seconds", 10)
    hg_api = HoneyGuideAPI(hg_host, hg_token, context_info=context_info, timeout_seconds=timeout_seconds)
    element_list = hg_api.get_generic_collection_elements(batch_size=batch_size, max_count=max_count)
    json_ret["summary"]["msg"] = hg_api.summary["msg"]
    json_ret["summary"]["statusCode"] = hg_api.summary["statusCode"]
    if hg_api.summary["statusCode"] == 0:
        json_ret["data"]["elements"] = element_list
        json_ret["data"]["count"] = len(element_list)
        json_ret["summary"]["msg"] = "获取成功"
    return json_ret

def add_generic_collection_item(params, assets, context_info):
    # 向通用集合中添加条目
    json_ret = {
        "code": 200, 
        "msg": "", 
        "data": {
            "duplicated": False
        }, 
        "summary": {
            "statusCode": -1, 
            "msg": ""
        }
    }

    hg_host = assets["hg_host"].strip().strip("/")
    hg_token = assets["hg_token"].strip()
    timeout_seconds = assets.get("timeout_seconds", 10)
    hg_api = HoneyGuideAPI(hg_host, hg_token, context_info=context_info, timeout_seconds=timeout_seconds)
    collection_name = params.get("collection_name", "")
    element_value = params.get("element_value", "")
    element_remark = params.get("element_remark", "")
    if collection_name == "" or element_value == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "collection_name, element_value不能为空"
        return json_ret
    
    element_remark = params.get("element_remark", "")
    update_if_exist = params.get("update_if_exist", False)
    add_element_result = hg_api.add_generic_collection_element(collection_name=collection_name,element_value=element_value, element_remark=element_remark, update_if_exist=update_if_exist)
    json_ret["summary"]["statusCode"] = hg_api.summary["statusCode"]
    json_ret["summary"]["msg"] = hg_api.summary["msg"]
    if add_element_result:
        json_ret["summary"]["statusCode"] = 0
        json_ret["data"]["duplicated"] = hg_api.summary["duplicated"]
    return json_ret

def get_generic_collection_element_info(params, assets, context_info):
    # 获取通用集合元素信息
    json_ret = {
        "code": 200, 
        "msg": "", 
        "data": {
            "createdBy": "",
            "modifiedBy": "",
            "createdNickName": "",
            "modifiedNickName": "",
            "createTime": "",
            "updateTime": "",
            "id": 0,
            "value": "",
            "collectionId": 0,
            "collectionName": "",
            "remark": "",
            "expireTime": "",
            "expireTimeStr": "",
            "effectiveTime": None,
            "effectiveTimeStr": None
        },
        "summary": {
            "statusCode": -1, 
            "msg": ""
        }
    }

    hg_host = assets["hg_host"].strip().strip("/")
    hg_token = assets["hg_token"].strip()
    timeout_seconds = assets.get("timeout_seconds", 10)
    hg_api = HoneyGuideAPI(hg_host, hg_token, context_info=context_info, timeout_seconds=timeout_seconds)
    collection_id = params.get("collection_id", 0)
    collection_name = params.get("collection_name", "")
    element_value = params.get("element_value", "")
    if collection_id == 0 and collection_name == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "collection_id和collection_name不能同时为空"
        return json_ret
    if element_value == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "element_value不能为空"
        return json_ret
    
    if collection_id > 0:
        json_element_info = hg_api.get_generic_collection_element_info_by_value(collection_id=collection_id, element_value=element_value)
    else:
        json_element_info = hg_api.get_generic_collection_element_info_by_value(collection_name=collection_name, element_value=element_value)
    
    json_element_info = hg_api.get_generic_collection_element_info_by_value(collection_id, collection_name, element_value)
    json_ret["summary"]["statusCode"] = hg_api.summary["statusCode"]
    json_ret["summary"]["msg"] = hg_api.summary["msg"]
    if 'id' in json_element_info.keys()  and json_element_info['id'] > 0:
        json_ret["summary"]["statusCode"] = 0
        json_ret["summary"]["msg"] = "元素信息获取成功"
        json_ret["data"] = json_element_info
    return json_ret

def update_generic_collection_element(params, assets, context_info):

    # 更新通用集合元素信息
    json_ret = {
        "code": 200, 
        "msg": "", 
        "data": {}, 
        "summary": {
            "statusCode": -1, 
            "msg": ""
        }
    }

    hg_host = assets["hg_host"].strip().strip("/")
    hg_token = assets["hg_token"].strip()
    timeout_seconds = assets.get("timeout_seconds", 10)
    hg_api = HoneyGuideAPI(hg_host, hg_token, context_info=context_info, timeout_seconds=timeout_seconds)
    collection_name = params.get("collection_name", "")
    element_value = params.get("element_value", "")
    element_remark = params.get("element_remark", "")
    if collection_name == "" or element_value == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "collection_name和element_value不能为空"
        return json_ret

    update_result = hg_api.update_generic_collection_element_by_value(collection_name=collection_name, element_value=element_value, element_remark=element_remark)
    json_ret["summary"]["statusCode"] = hg_api.summary["statusCode"]
    json_ret["summary"]["msg"] = hg_api.summary["msg"]
    if update_result:
        json_ret["summary"]["statusCode"] = 0
        json_ret["summary"]["msg"] = "元素信息更新成功"
    return json_ret

def delete_generic_collection_element(params, assets, context_info): 
    # 删除通用集合元素
    json_ret = {
        "code": 200, 
        "msg": "", 
        "data": {}, 
        "summary": {
            "statusCode": -1, 
            "msg": ""
        }
    }

    hg_host = assets["hg_host"].strip().strip("/")
    hg_token = assets["hg_token"].strip()
    timeout_seconds = assets.get("timeout_seconds", 10)
    hg_api = HoneyGuideAPI(hg_host, hg_token, context_info=context_info, timeout_seconds=timeout_seconds)
    collection_name = params.get("collection_name", "")
    element_value = params.get("element_value", "")
    if collection_name == "" or element_value == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "collection_name和element_value不能为空"
        return json_ret
    delete_result = hg_api.delete_generic_collection_element_by_value(collection_name, element_value)
    json_ret["summary"]["statusCode"] = hg_api.summary["statusCode"]
    json_ret["summary"]["msg"] = hg_api.summary["msg"]
    if delete_result:
        json_ret["summary"]["statusCode"] = 0
    return json_ret

def check_generic_collection_element_exists(params, assets, context_info):
    # 检查通用集合元素是否存在
    json_ret = {
        "code": 200, 
        "msg": "",  
        "data": {
            "element_exists": False
        },
        "summary": {            
            "statusCode": -1, 
            "msg": ""
        }
    }

    hg_host = assets["hg_host"].strip().strip("/")
    hg_token = assets["hg_token"].strip()
    timeout_seconds = assets.get("timeout_seconds", 10)
    hg_api = HoneyGuideAPI(hg_host, hg_token, context_info=context_info, timeout_seconds=timeout_seconds)
    collection_name = params.get("collection_name", "")
    element_value = params.get("element_value", "")
    if element_value == 0 or collection_name == "":
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = "collection_name和element_value不能为空"
        return json_ret
    element_exists = hg_api.check_generic_collection_element_exists(collection_name=collection_name, element_value=element_value)
    json_ret["summary"]["statusCode"] = hg_api.summary["statusCode"]
    json_ret["summary"]["msg"] = hg_api.summary["msg"]
    if element_exists:
        json_ret["data"]["element_exists"] = True
        json_ret["summary"]["statusCode"] = 0
    else:
        json_ret["data"]["element_exists"] = False
        json_ret["summary"]["statusCode"] = 404
    return json_ret

def health_check(params, assets, context_info):
    # 健康检查
    json_ret = {
        "code": 200, 
        "msg": "", 
        "data": {}, 
        "summary": {
            "statusCode": -1, 
            "msg": ""
        }
    }
    hg_host = assets["hg_host"].strip().strip("/")
    hg_token = assets["hg_token"].strip()
    timeout_seconds = assets.get("timeout_seconds", 10)
    hg_api = HoneyGuideAPI(hg_host, hg_token, context_info=context_info, timeout_seconds=timeout_seconds)
    health_check_result = hg_api.health_check()
    json_ret["summary"]["statusCode"] = hg_api.summary["statusCode"]
    json_ret["summary"]["msg"] = hg_api.summary["msg"]
    if health_check_result:
        json_ret["summary"]["statusCode"] = 200
        json_ret["summary"]["msg"] = "健康检查成功"
    return json_ret