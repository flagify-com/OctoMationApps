# -*- coding: utf-8 -*-
import time
from core_activelist import ActiveListManager
from action_sdk_for_cache.action_cache_sdk import HoneyGuide
import re

def add_record_to_active_list(params, assets, context_info):
    """添加记录到活动列表"""

    # 活动列表的名称
    activelist_name = params["activelist_name"]
    # 活动列表元素的key名称
    item_key = params["item_key"]

    # 活动列表元素的value值
    item_value = params["item_value"]

    # 活动列表元素的备注信息
    item_remark = "" if "item_remark" not in params.keys() or params["item_remark"] == "" or params["item_remark"] is None else params["item_remark"]
    
    replace_if_exists = params.get("replace_if_exists", False)
    try:
        replace_if_exists = bool(replace_if_exists)
    except :
        replace_if_exists = False

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"err_code": 0, "err_msg": ""}}
    if not re.compile(r'^[a-zA-Z0-9_\-]+$').match(activelist_name):
        json_ret["data"]["err_code"] = 400
        json_ret["data"]["err_msg"] = "活动列表名称不符合要求：字母、数字、下划线、中划线的组合"
        json_ret["data"]["activelist_name"] = activelist_name
        return json_ret

    if item_key == "" or item_key is None or item_value == "" or item_value is None:
        json_ret["data"]["err_code"] = 400
        json_ret["data"]["err_msg"] = "参数错误"
        json_ret["data"]["activelist_name"] = activelist_name
        json_ret["data"]["item_key"] = item_key
        json_ret["data"]["item_value"] = item_value
        json_ret["data"]["item_remark"] = item_remark
        return json_ret

    hg_client = HoneyGuide(context_info)
    activelist = ActiveListManager(hg_client)

    '''添加函数实现
    
    '''
    if activelist.add_record_to_active_list(activelist_name, item_key, item_value, item_remark, replace_if_exists) == True:
        json_ret["data"]["err_code"] = 0
        json_ret["data"]["err_msg"] = "添加记录到活动列表成功"
        json_ret["data"]["activelist_name"] = activelist_name
        json_ret["data"]["item_key"] = item_key
        json_ret["data"]["item_value"] = item_value
        json_ret["data"]["item_remark"] = item_remark
    else:
        json_ret["data"]["err_code"] = 1
        json_ret["data"]["err_msg"] = "添加记录到活动列表失败\n" + activelist.msg
        json_ret["data"]["activelist_name"] = activelist_name
        json_ret["data"]["item_key"] = item_key
        json_ret["data"]["item_value"] = item_value
        json_ret["data"]["item_remark"] = item_remark

    return json_ret 

def count_records_within_time_window(params, assets, context_info):
    """统计时间窗口内记录行数"""


    # 活动列表的名称
    activelist_name = params["activelist_name"]

    # 活动列表元素的key名称
    item_key = params.get("item_key", "*")

    # 活动列表时间窗口的截止时间，默认为当前时间。
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) if "end_time" not in params.keys() or params["end_time"] == "" else params["end_time"]

    # 向前查询活动列表时间窗口长度，单位是分钟。
    time_delta_minute = 120 if "time_delta_minute" not in params.keys() or params["time_delta_minute"] == "" else params["time_delta_minute"]
    try:
        time_delta_minute = int(time_delta_minute)
    except:
        time_delta_minute = 120

    time_delta_minute_str = str(time_delta_minute) + "m"
    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"err_code": 0, "err_msg": "", "record_count": 0}}

    if not re.compile(r'^[a-zA-Z0-9_\-]+$').match(activelist_name):
        json_ret["data"]["err_code"] = 400
        json_ret["data"]["err_msg"] = "活动列表名称不符合要求：字母、数字、下划线、中划线的组合"
        json_ret["data"]["activelist_name"] = activelist_name
        return json_ret

    '''添加函数实现
    
    '''
    hg_client = HoneyGuide(context_info)
    activelist = ActiveListManager(hg_client)
    record_counts = activelist.count_records_within_time_window(activelist_name, item_key, end_time, time_delta_minute_str)    
    if record_counts is not None and record_counts >= 0:
        json_ret["data"]["err_code"] = 0
        json_ret["data"]["err_msg"] = "查询成功，记录数：{}".format(record_counts)
        json_ret["data"]["record_count"] = record_counts
    else:
        json_ret["data"]["err_code"] = 1
        json_ret["data"]["err_msg"] = "查询失败\n" + activelist.msg 
        json_ret["data"]["record_count"] = 0

    return json_ret 

def remove_record_from_active_list(params, assets, context_info):
    """从活动列表中移除记录"""


    # 活动列表名称
    activelist_name = params["activelist_name"]

    # 活动列表元素的key值
    item_key = params["item_key"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"err_code": 0, "err_msg": ""}}

    '''添加函数实现
    
    '''

    if not re.compile(r'^[a-zA-Z0-9_\-]+$').match(activelist_name):
        json_ret["data"]["err_code"] = 400
        json_ret["data"]["err_msg"] = "活动列表名称不符合要求：字母、数字、下划线、中划线的组合"
        json_ret["data"]["activelist_name"] = activelist_name
        return json_ret

    hg_client = HoneyGuide(context_info)
    activelist = ActiveListManager(hg_client)
    if activelist.remove_record_from_active_list(activelist_name, item_key):    
        json_ret["data"]["err_code"] = 0
        json_ret["data"]["err_msg"] = "从活动列表中移除记录成功"
        json_ret["data"]["activelist_name"] = activelist_name
        json_ret["data"]["item_key"] = item_key
    else:
        json_ret["data"]["err_code"] = 1
        json_ret["data"]["err_msg"] = "从活动列表中移除记录失败\n" + activelist.msg
        json_ret["data"]["activelist_name"] = activelist_name
        json_ret["data"]["item_key"] = item_key


    return json_ret 

def initialize_active_list_table(params, assets, context_info):
    """初始化活动列表的数据库表"""


    # 活动列表的名称。不同的应用场景，请务必区分。
    activelist_name = None if "activelist_name" not in params.keys() or params["activelist_name"] == "" or params["activelist_name"] is None else params["activelist_name"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"err_code": 0, "err_msg": ""}}

    if not re.compile(r'^[a-zA-Z0-9_\-]+$').match(activelist_name):
        json_ret["data"]["err_code"] = 400
        json_ret["data"]["err_msg"] = "活动列表名称不符合要求：字母、数字、下划线、中划线的组合"
        json_ret["data"]["activelist_name"] = activelist_name
        return json_ret


    '''添加函数实现
    
    '''
    hg_client = HoneyGuide(context_info)
    activelist = ActiveListManager(hg_client)
    if activelist.initialize_active_list_table(table_name=activelist_name):
        json_ret["data"]["err_code"] = 0
        json_ret["data"]["err_msg"] = "初始化活动列表成功"
        json_ret["data"]["activelist_name"] = activelist_name    
    else:
        json_ret["data"]["err_code"] = 1
        json_ret["data"]["err_msg"] = "初始化活动列表失败." + activelist.msg
        json_ret["data"]["activelist_name"] = activelist_name

    return json_ret

def get_records_time_trend(params, assets, context_info):
    """获取活动列表元素的时间趋势"""
        # 活动列表的名称
    activelist_name = params.get("activelist_name", "")
    # 活动列表元素的key名称
    item_key = params.get("item_key", "")
    time_unit = params.get("time_unit", "DAY")
    unit_amount = int(params.get("unit_amount", 7))
    # 返回值
    json_ret = {
        "code": 200, 
        "msg": "",
        "data": {
            "err_code": 0, 
            "err_msg": "", 
            "activelist_name":activelist_name,
            "total_count": -1,
            "records": []
        }
    }

    if not re.compile(r'^[a-zA-Z0-9_\-]+$').match(activelist_name): 
        json_ret["data"]["err_code"] = 400
        json_ret["data"]["err_msg"] = "活动列表名称不符合要求：字母、数字、下划线、中划线的组合"
        json_ret["data"]["activelist_name"] = activelist_name
        return json_ret

    '''添加函数实现
    
    '''
    hg_client = HoneyGuide(context_info)
    activelist = ActiveListManager(hg_client)
    record_count_result = activelist.get_records_time_trend(activelist_name, item_key, time_unit, unit_amount)
    if record_count_result is not None:
        json_ret["data"]["err_code"] = 0
        json_ret["data"]["err_msg"] = "查询成功"
        # json_ret["data"]["records"] = record_counts
        json_ret['data']["total_count"] = len(record_count_result)
        for record in record_count_result:
            dict_item ={
                "xTime": record[0],
                "xCount": record[1]
            }
            json_ret["data"]["records"].append(dict_item)
    else:
        json_ret["data"]["err_code"] = 1
        json_ret["data"]["err_msg"] = "查询失败\n" + activelist.msg
        json_ret["data"]["record_count"] = -1
    return json_ret 

def quick_view_active_list(params, assets, context_info):
    """快速查看活动列表"""
    activelist_name = params.get("activelist_name", "")
    item_key = params.get("item_key", "*")

    # 返回值
    json_ret = {
        "code": 200, 
        "msg": "",
        "data": {
            "err_code": 0, 
            "err_msg": "", 
            "activelist_name": activelist_name,
            "item_key": item_key,
            "total_count": -1,
            "records": []
        }
    }

    if not re.compile(r'^[a-zA-Z0-9_\-]+$').match(activelist_name):
        json_ret["data"]["err_code"] = 400
        json_ret["data"]["err_msg"] = "活动列表名称不符合要求：字母、数字、下划线、中划线的组合"
        json_ret["data"]["activelist_name"] = activelist_name
        return json_ret

    '''添加函数实现
    
    '''
    hg_client = HoneyGuide(context_info)
    activelist = ActiveListManager(hg_client)
    quick_view_result = activelist.quick_view_active_list(activelist_name, item_key)
    if quick_view_result is not None:
        json_ret["data"]["err_code"] = 0
        json_ret["data"]["err_msg"] = "查询成功"
        json_ret['data']["total_count"] = len(quick_view_result)
        for record in quick_view_result:
            dict_item ={
                "_key": record[0],
                "_value": record[1],
                "_remark": record[2],
                "create_time": record[3],
                "update_time": record[4]
            }
            json_ret["data"]["records"].append(dict_item)
    else:
        json_ret["data"]["err_code"] = 1
        json_ret["data"]["records"] = -1
        json_ret["data"]["err_msg"] = "查询失败\n" + activelist.msg
        
    return json_ret

def clear_active_list(params, assets, context_info):
    """清空活动列表"""

    activelist_name = None if "activelist_name" not in params.keys() or params["activelist_name"] == "" or params["activelist_name"] is None else params["activelist_name"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"err_code": 0, "err_msg": ""}}
    # 正则表达式匹配，activelist_name满足：字母、数字、下划线、中划线的组合
    if not re.compile(r'^[a-zA-Z0-9_\-]+$').match(activelist_name):
        json_ret["data"]["err_code"] = 400
        json_ret["data"]["err_msg"] = "活动列表名称不符合要求：字母、数字、下划线、中划线的组合"
        json_ret["data"]["activelist_name"] = activelist_name
        return json_ret
    
    hg_client = HoneyGuide(context_info)
    activelist = ActiveListManager(hg_client)
    if activelist.clear_active_list(activelist_name):
        json_ret["data"]["err_code"] = 0
        json_ret["data"]["err_msg"] = "清空活动列表成功！"
        json_ret["data"]["activelist_name"] = activelist_name
    else:
        json_ret["data"]["err_code"] = 500
        json_ret["data"]["err_msg"] = "清空活动列表失败！\n" + activelist.msg
        json_ret["data"]["activelist_name"] = activelist_name

    return json_ret

def delete_active_list(params, assets, context_info):
    """删除活动列表"""

    activelist_name = params.get("activelist_name", None)

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"err_code": 0, "err_msg": ""}}
    
    # 正则表达式匹配，activelist_name满足：字母、数字、下划线、中划线的组合
    if not re.compile(r'^[a-zA-Z0-9_\-]+$').match(activelist_name):
        json_ret["data"]["err_code"] = 400
        json_ret["data"]["err_msg"] = "活动列表名称不符合要求：字母、数字、下划线、中划线的组合"
        json_ret["data"]["activelist_name"] = activelist_name
        return json_ret
    
    hg_client = HoneyGuide(context_info)
    activelist = ActiveListManager(hg_client)
    if activelist.delete_active_list(activelist_name):
        json_ret["data"]["err_code"] = 0
        json_ret["data"]["err_msg"] = "删除活动列表成功！"
        json_ret["data"]["activelist_name"] = activelist_name
    else:
        json_ret["data"]["err_code"] = 500
        json_ret["data"]["err_msg"] = "删除活动列表失败！\n" + activelist.msg
        json_ret["data"]["activelist_name"] = activelist_name

    return json_ret

def list_all_active_lists(params, assets, context_info):
    """列举出所有活动列表"""
    json_ret = {"code": 200, "msg": "","data": {"err_code": 0, "err_msg": "", "activelists": []}}
    hg_client = HoneyGuide(context_info)
    activelist = ActiveListManager(hg_client)
    active_lists =  activelist.list_all_active_lists()
    if isinstance(active_lists, list):
        json_ret["data"]["err_code"] = 0
        json_ret["data"]["err_msg"] = "列举出所有活动列表成功！总数为：{}".format(len(active_lists))
        json_ret["data"]["activelists"] = active_lists
    else:
        json_ret["data"]["err_code"] = 500
        json_ret["data"]["err_msg"] = "列举出所有活动列表失败！\n" + activelist.msg
        json_ret["data"]["activelists"] = []

    return json_ret

def health_check(params, assets, context_info):
    """健康检查"""


    # 返回值
    json_ret = {"code": 200, "msg": "", "summary": { "msg": "健康检查成功", "statusCode": 200 }}
    '''添加函数实现
    
    '''
    hg_client = HoneyGuide(context_info)
    activelist = ActiveListManager(hg_client)
    try:
        result = activelist.get_db_connection()
        if result is not None:
            json_ret["summary"]["statusCode"] = 200
            json_ret["summary"]["msg"] = "健康检查成功"
        else:
            json_ret["summary"]["statusCode"] = 500
            json_ret["summary"]["msg"] =  "健康检查失败:" + activelist.msg
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] =  "健康检查失败:" + str(e)  

    return json_ret

