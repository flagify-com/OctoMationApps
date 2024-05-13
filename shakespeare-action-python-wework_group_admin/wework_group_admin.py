# -*- coding: utf-8 -*-
from core_wework_group_admin import WeWorkGroupAdmin

# 应用ID，直接写死了。

APPID = 'wework_group_admin'

def create_appchat_group(params, assets, context_info):
    """创建群聊会话"""
    # 企业微信API服务地址BaseURI
    apiserver_base_uri = assets["apiserver_base_uri"].strip()
    if apiserver_base_uri.endswith('/'):
        apiserver_base_uri = apiserver_base_uri[:-1]

    # 企业组织ID
    corpid = assets["corpid"].strip()
    # 应用的凭证密钥，注意应用需要是启用状态
    corpsecret = assets["corpsecret"].strip()

    # 群聊名，最多50个utf8字符，超过将截断
    group_name = params.get("group_name", None).strip()

    # 指定群主的id。如果不指定，系统会随机从userlist中选一人作为群主
    group_owner = params.get("group_owner", None).strip()

    # 群成员id，逗号（,）分隔，至少2人，至多2000人
    group_userids = params.get("group_userids", '').strip().replace("，", ",").split(",")
    group_userids = [u.strip() for u in group_userids if u.strip()]

    # 群id，群聊的唯一标志，不能与已有的群重复；字符串类型，最长32个字符。只允许字符0-9及字母a-zA-Z。如果不填，系统会随机生成
    group_chatid = params.get("group_chatid", None)

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"errcode": -1, "errmsg": "Unknown Error", "chatid": ""}}
    if len(group_userids) < 2:
        json_ret['data']['errcode'] = -1
        json_ret['data']['errmsg'] = "Group userids must be at least 2"
        return json_ret

    wework_group_admin = WeWorkGroupAdmin(APPID, corpid, corpsecret, apiserver_base_uri)
    json_ret['data'] = wework_group_admin.create_group(group_userids, group_name, group_owner, group_chatid)
    return json_ret


def update_appchat_group(params, assets, context_info):
    """修改群聊会话"""
    # 企业微信API服务地址BaseURI
    apiserver_base_uri = assets["apiserver_base_uri"].strip()
    if apiserver_base_uri.endswith('/'):
        apiserver_base_uri = apiserver_base_uri[:-1]

    # 企业组织ID
    corpid = assets["corpid"].strip()
    # 应用的凭证密钥，注意应用需要是启用状态
    corpsecret = assets["corpsecret"].strip()

    # 群聊id
    group_chatid = params.get("group_chatid", None)

    # 新的群聊名。若不需更新，请忽略此参数。最多50个utf8字符，超过将截断
    if "group_name" in params.keys() and params["group_name"] != "" and params["group_name"] is not None: group_name= params["group_name"]

    # 新群主的id。若不需更新，请忽略此参数。课程群聊群主必须在设置的群主列表内
    if "group_owner" in params.keys() and params["group_owner"] != "" and params["group_owner"] is not None: group_owner= params["group_owner"]

    # 群聊名，最多50个utf8字符，超过将截断
    group_name = params.get("group_name", None)

    # 指定群主的id。如果不指定，系统会随机从userlist中选一人作为群主
    group_owner = params.get("group_owner", None)

    # 添加成员的id，逗号（,）分隔
    group_add_userids = params.get("group_add_userids", '').strip().replace("，", ",").split(",")
    group_add_userids = [u.strip() for u in group_add_userids if u.strip()]

    # 移除成员的id，逗号（,）分隔
    group_del_userids = params.get("group_del_userids", '').strip().replace("，", ",").split(",")
    group_del_userids = [u.strip() for u in group_del_userids if u.strip()]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"errcode": -1, "errmsg": "Unknown Error"}}
    if group_chatid is None or group_chatid == "":
        json_ret['data']['errcode'] = -1
        json_ret['data']['errmsg'] = "Group chatid is required"
        return json_ret

    wework_group_admin = WeWorkGroupAdmin(APPID, corpid, corpsecret, apiserver_base_uri)
    json_ret['data'] = wework_group_admin.update_group(group_chatid, group_name, group_owner, group_add_userids, group_del_userids)
    return json_ret


def get_appchat_group(params, assets, context_info):
    """获取群聊会话"""

    # 企业微信API服务地址BaseURI
    apiserver_base_uri = assets["apiserver_base_uri"].strip()
    if apiserver_base_uri.endswith('/'):
        apiserver_base_uri = apiserver_base_uri[:-1]

    # 企业组织ID
    corpid = assets["corpid"].strip()
    # 应用的凭证密钥，注意应用需要是启用状态
    corpsecret = assets["corpsecret"].strip()

    # 群聊id
    group_chatid = params.get("group_chatid", None)

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"errcode": -1, "errmsg": "Unknown Error", "chatid": "", "name": "", "owner": "", "userlist": []}}

    if group_chatid is None or group_chatid == "":
        json_ret['data']['errcode'] = -1
        json_ret['data']['errmsg'] = "Group chatid is required"
        return json_ret

    wework_group_admin = WeWorkGroupAdmin(APPID, corpid, corpsecret, apiserver_base_uri)
    json_ret['data'] = wework_group_admin.get_group_chat_info(group_chatid)
    if 'chat_info' in json_ret['data'].keys():
        chat_info = json_ret['data']['chat_info']
        json_ret['data']['chatid'] = chat_info['chatid']
        json_ret['data']['name'] = chat_info['name']
        json_ret['data']['owner'] = chat_info['owner']
        json_ret['data']['userlist'] = chat_info['userlist']
        # del json_ret['data']['chat_info']
    return json_ret

def send_appchat_group_text(params, assets, context_info):
    """发送群聊文本消息"""

    # 企业微信API服务地址BaseURI
    apiserver_base_uri = assets["apiserver_base_uri"].strip()
    if apiserver_base_uri.endswith('/'):
        apiserver_base_uri = apiserver_base_uri[:-1]

    # 企业组织ID
    corpid = assets["corpid"].strip()
    # 应用的凭证密钥，注意应用需要是启用状态
    corpsecret = assets["corpsecret"].strip()

    # 群ID
    group_chatid = params.get("group_chatid", None)

    # 消息内容，最长不超过2048个字节
    text = params.get("text", None)

    # 是保密消息，0表示否，1表示是，默认0
    safe = 0 if "safe" not in params.keys() or params["safe"] == "" else int(params["safe"])
    if safe not in [0, 1]:
        safe = 0

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"errcode": -1, "errmsg": "Unknown Error"}}
    if group_chatid is None or group_chatid == "":
        json_ret['data']['errcode'] = -1
        json_ret['data']['errmsg'] = "Group chatid is required"
        return json_ret

    if text is None or text == "":
        json_ret['data']['errcode'] = -1
        json_ret['data']['errmsg'] = "Text is required"
        return json_ret

    wework_group_admin = WeWorkGroupAdmin(APPID, corpid, corpsecret, apiserver_base_uri)
    json_ret['data'] = wework_group_admin.send_group_text_message(group_chatid, text, safe)
    return json_ret



