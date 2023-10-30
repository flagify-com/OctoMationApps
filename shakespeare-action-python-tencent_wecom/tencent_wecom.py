# -*- coding: utf-8 -*-
import json
import traceback
import socket
import requests
from other_func import *
from user_info_book import *
import datetime


"""
初始化数据
"""
# 文件操作类型
file_operate_type = {
    101: '上传',
    102: '新建文件夹',
    103: '下载',
    104: '更新',
    105: '星标',
    106: '移动',
    107: '复制',
    108: '重命名',
    109: ' 删除',
    110: '恢复',
    111: '彻底删除',
    112: '转发到企业微信',
    113: '通过链接下载',
    114: '获取分享链接',
    115: '修改分享链接',
    116: '关闭分享链接',
    117: '收藏',
    118: '新建文档',
    119: '新建表格',
    121: '打开',
    124: '导出文件',
    127: '添加文件成员',
    128: '修改文件成员权限',
    129: '移除文件成员',
    130: '设置文档水印',
    131: '修改企业内权限',
    132: '修改企业外权限',
    133: '添加快捷入口',
    134: '转发到微信',
    135: '预览',
    136: '权限管理',
    139: '安全设置',
    140: '通过邮件分享',
    142: '离职成员文件转交'
}
# 文件来源类型
file_source_type = {401: '聊天', 402: '邮件', 403: '文档', 404: '微盘', 405: '日程'}


def str_to_timestamp(str_time=None, format='%Y-%m-%d %H:%M:%S'):
    if str_time:
        time_tuple = time.strptime(str_time, format)
        result = time.mktime(time_tuple)
        return int(result)
    return int(time.time())


def health_check(params, assets, context_info):
    """检查企业微信的消息是否正常"""
    corp_id = assets["corp_id"]
    corp_secret = assets["corp_secret"]
    # 企业应用的id
    agent_id = assets["agent_id"]

    # 指定接受消息的成员id
    to_user = assets["to_user"]
    # 获取 token
    token = Get_Token(corp_id, corp_secret)
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
    data = {
        "touser": to_user,
        "msgtype": "text",
        "agentid": agent_id,
        "text": {
            "content": "企微（SOAR平台）资源健康（发送消息API接口）检查消息，请忽略！"
        },
        "safe": 0
    }
    try:
        r = requests.post(url=url, data=json.dumps(data))
        # 返回值
        resp_json = r.json()
        if r.status_code == 200 and str(resp_json['errcode']) == "0":
            json_ret = {"code": 200, "msg": "", "data": resp_json, "summary": {"statusCode": 200, "msg": "资源健康"}}
        else:
            json_ret = {"code": r.status_code, "msg": "异常", "data": resp_json, "summary": {"statusCode": int(resp_json['errcode']), "msg": "资源异常"}}
    except Exception as e:
        json_ret = {"code": 500, "msg": "请求异常，错误:{}".format(e)}
    return json_ret


def Get_Token(corp_id, corp_secret):
    """获取 token"""
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}".format(corp_id, corp_secret)
    r = requests.get(url=url)
    if r.status_code != 200:
        return ''

    token = r.json()['access_token']
    return token


def Send_Message(params, assets, context_info):
    """消息发送"""
    corp_id = assets["corp_id"]
    corp_secret = assets["corp_secret"]
    # 企业应用的id
    agent_id = assets["agent_id"]
    # 消息内容
    content = params["content"]
    # 指定接受消息的成员id
    to_user = params["to_user"]
    # 获取 token
    token = Get_Token(corp_id, corp_secret)
    # 发送消息
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
    data = {
        "touser": to_user,
        "msgtype": "text",
        "agentid": agent_id,
        "text": {
            "content": content
        },
        "safe": 0
    }
    try:
        r = requests.post(url=url, data=json.dumps(data))
        # 返回值
        if r.status_code == 200:
            json_ret = {"code": 200, "msg": "", "data": r.json()}
        else:
            json_ret = {"code": r.status_code, "msg": "异常", "data": r.json()}
    except Exception as e:
        json_ret = {"code": 500, "msg": "请求异常，错误:{}".format(e)}
    return json_ret


def get_user_device(params, assets, context_info):
    """
    开发者：wuk 开发时间戳：1692775241
    获取成员设备
    :param 变量名称: str 入参注解
    :return: 出参注解
    """
    corp_id = assets["corp_id"]
    corp_secret = assets["corp_secret"]
    # 指定需要获取设备的成员id
    to_user = params["to_user"]
    type_device = params["type_device"]
    # 获取 token
    token = Get_Token(corp_id, corp_secret)
    # 发送消息
    url = "https://qyapi.weixin.qq.com/cgi-bin/security/trustdevice/get_by_user?access_token={}".format(token)
    data = {
        "last_login_userid": to_user,
        "type": type_device
    }
    try:
        r = requests.post(url=url, data=json.dumps(data))
        # 返回值
        if r.status_code == 200:
            json_ret = {"code": 200, "msg": "", "data": r.json()}
        else:
            json_ret = {"code": r.status_code, "msg": "异常", "data": r.json()}
    except Exception as e:
        json_ret = {"code": 500, "msg": "请求异常，错误:{}".format(e)}

    return json_ret


def get_device_info(params, assets, context_info):
    """
    开发者：wuk 开发时间戳：1692775241
    获取设备信息
    :param 变量名称: str 入参注解
    :return: 出参注解
    """
    corp_id = assets["corp_id"]
    corp_secret = assets["corp_secret"]
    type_device = params["type_device"]
    # 获取 token
    token = Get_Token(corp_id, corp_secret)
    # 发送消息
    url = "https://qyapi.weixin.qq.com/cgi-bin/security/trustdevice/list?access_token={}".format(token)
    req_data = {
        "limit": 100,
        "type": type_device
    }
    try:
        r = requests.post(url=url, data=json.dumps(req_data))
        # 返回值
        if r.status_code == 200:
            data = []
            res_json = json.loads(r.text)
            data += res_json['device_list']
            while res_json.get("next_cursor", False) and res_json['errmsg'] == "ok":
                req_data["cursor"] = res_json.get("next_cursor")
                r = requests.post(url=url, data=json.dumps(req_data))
                data += res_json['device_list']
            json_ret = {"code": 200, "msg": "", "data": data}

        else:
            json_ret = {"code": r.status_code, "msg": "异常", "data": r.json()}
    except Exception as e:
        json_ret = {"code": 500, "msg": "请求异常，错误{}:{}".format(e.__traceback__.tb_lineno, str(e))}
    return json_ret


def get_file_oper_record(params, assets, context_info):
    """
    开发者：wuk 开发时间戳：1692775241
    文件防泄漏
    :param 变量名称: str 入参注解
    :return: 出参注解
    """
    json_ret = {"code": 200, "msg": "动作运行正常", "summary": {"statusCode": 404, "msg": "动作逻辑执行异常"}, "data": {"count": 0}}

    corp_id = assets["corp_id"]
    corp_secret = assets["corp_secret"]
    # 指定需要获取设备的成员id
    # to_user = str(params["to_user"]).split(',')
    # type_source = params["type_source"]
    # s_source=params['s_source']
    # 获取 token

    # 接口起始时间参数计算
    # start_time = int(time_strp(params['start_time']) / 1000) if "start_time" in params.keys() and len(
    #     params['start_time']) != 0 else int(time.time()) - 60 * 60
    # end_time = int(time_strp(params['end_time']) / 1000) if "end_time" in params.keys() and len(
    #     params['end_time']) != 0 else int(time.time())

    timedelta_ = params['timedelta'] if 'timedelta' in params.keys() and params['timedelta'] and params['timedelta'] != "null" and params['timedelta'] != '' else None
    timedelta_unit = params['timedelta_unit']

    # 是否需要socket推送消息
    socket_addr = params['socket_addr'] if 'socket_addr' in params.keys() and params['socket_addr'] != 'null' else None
    socket_port = params['socket_port'] if 'socket_port' in params.keys() and params['socket_port'] != 'null' else None
    socket_protocol = params['socket_protocol'] if 'socket_protocol' in params.keys() and params['socket_protocol'] != 'null' else None
    socket_timeout = params['socket_timeout'] if 'socket_timeout' in params.keys() and params['socket_timeout'] != 'null' else None

    # # 结束时间
    time_to = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if "end_time" not in params.keys() or params[
        'end_time'] == "" or params['end_time'] is None or params['end_time'] == 'null' else params["end_time"]

    # 推移时间计算开始时间字符和格式
    if timedelta_ is not None:
        # 开始时间
        if timedelta_unit == 'minutes':
            time_from = (datetime.datetime.now() - datetime.timedelta(minutes=timedelta_)).strftime("%Y-%m-%d %H:%M:%S")
        elif timedelta_unit == 'hours':
            time_from = (datetime.datetime.now() - datetime.timedelta(hours=timedelta_)).strftime("%Y-%m-%d %H:%M:%S")
        elif timedelta_unit == 'seconds':
            time_from = (datetime.datetime.now() - datetime.timedelta(seconds=timedelta_)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            time_from = (datetime.datetime.now() - datetime.timedelta(days=timedelta_)).strftime("%Y-%m-%d %H:%M:%S")

    else:
        if not params['time_from'] or params['time_from'] is None or params['time_from'] == 'null':
            return {"code": 200, "msg": "动作运行正常", "summary": {"statusCode": 404, "msg": "时间范围和时间段参数必须选一种方式调用该动作"}}

        # 手动输入开始时间
        time_from = params["start_time"]

    # 开始时间计算处理
    timestamp_from = str_to_timestamp(time_from) - int(params['forward_time']) if 'forward_time' in params.keys() \
        else str_to_timestamp(time_from)

    timestamp_to = str_to_timestamp(time_to)

    # print("time_from: ", time_from)
    # print("time_to: ", time_to)
    #
    # print("timestamp_from: ", timestamp_from)
    # print("timestamp_to: ", timestamp_to)

    access_token = Get_Token(corp_id, corp_secret)
    # other_corp_secret = params['other_corp_secret'] if 'other_corp_secret' in params.keys() else ''
    # user_token = Get_Token(corp_id, other_corp_secret)
    # 发送消息
    url = "https://qyapi.weixin.qq.com/cgi-bin/security/get_file_oper_record?access_token={}".format(access_token)

    # 查询所有文件日志
    if params['filter_file_type'] == 0:

        data = {
            # "start_time": start_time,
            "start_time": timestamp_from,
            # "end_time": end_time,
            "end_time": timestamp_to,
            "limit": params['limit'] if 'limit' in params.keys() and params['limit'] != 'null' else 1000
        }
    # 查询部分文件日志告警
    else:
        data = {
            # "start_time": start_time,
            "start_time": timestamp_from,
            # "end_time": end_time,
            "end_time": timestamp_to,
            "operation": {
                "type": params['filter_file_type'],
                #"source": 401
            },
            "limit": params['limit'] if 'limit' in params.keys() and params['limit'] != 'null' else 1000
        }

    setSock = None

    try:
        message = ""
        res_data = []

        if socket_port is not None and socket_addr is not None and socket_protocol is not None:
            if socket_protocol == 'UDP':
                setSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                setSock.connect((socket_addr, socket_port))
                # ss = (msg + '\n').encode()
                # setSock.send(ss)
                # return "发送UDP成功"
            elif socket_protocol == 'TCP':
                setSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                setSock.settimeout(socket_timeout)

                setSock.connect((socket_addr, socket_port))  # TCP
                # ss = (msg + '\n').encode()
                # ss = (msg + '\n').encode('raw-unicode-escape') #中文转
                # print(setSock.send(ss))
                # message = "发送TCP成功"
            else:
                json_ret['summary']['statusCode'] = 403
                json_ret['summary']['msg'] = f'暂不支持该协议：{socket_protocol}'
                return json_ret

        first_resp = requests.post(url=url, data=json.dumps(data), timeout=assets['conn_time_out'], verify=assets['verify_server_cert'])
        # print(1111, r.status_code)
        # print(1111, r.text)
        # 返回值
        if first_resp.status_code == 200:
            first_res_json = first_resp.json()
            # res=res_json

            res_data += first_res_json['record_list']
            if first_res_json['has_more'] and first_res_json['errmsg'] == "ok":
                data['cursor'] = first_res_json['next_cursor']

                r = requests.post(url=url, data=json.dumps(data), timeout=assets['conn_time_out'], verify=assets['verify_server_cert'])
                # print(2222, r.status_code)
                # print(2222, r.text)
                res_json = r.json()
                # res=res_json
                if res_json['errmsg'] != "ok":
                    # 请求失败
                    pass
                else:
                    res_data += res_json['record_list']
            else:
                json_ret['summary']['statusCode'] = 404
                json_ret['summary']['msg'] = f'查询数据失败：{first_res_json}'

            send_success_count = 0
            not_user_id_count = 0
            request_api_fail_count = 0

            for obj_info in res_data:

                # TODO：不存在userid待处理
                if 'userid' not in obj_info.keys():
                    not_user_id_count += 1
                    continue

                # 修改数据来源
                user_info = use_userid_get_user_info(token=access_token, user_id=obj_info['userid'], time_out=assets['conn_time_out'])
                # print("user_info66666: ", user_info)

                if user_info['errmsg'] == "ok":
                    obj_info['operation']['source'] = file_source_type[obj_info['operation']['source']] if 'source' in obj_info['operation'].keys() else ''
                    obj_info['operation']['type'] = file_operate_type[obj_info['operation']['type']] if 'type' in obj_info['operation'].keys() else ''
                    obj_info.update(user_info)
                    if socket_protocol == 'UDP' and setSock is not None:
                        setSock.send((json.dumps(obj_info, ensure_ascii=False) + '\n').encode())
                        send_success_count += 1
                        # return "发送UDP成功"

                    if socket_protocol == 'TCP' and setSock is not None:
                        # ss = (msg + '\n').encode('raw-unicode-escape') #中文转
                        # print(setSock.send(ss))
                        # message = "发送TCP成功"
                        setSock.send((json.dumps(obj_info, ensure_ascii=False) + '\n').encode())
                        send_success_count += 1
                        # return "发送UDP成功"
                else:
                    request_api_fail_count += 1

            # print("res_data: ", len(res_data), res_data)
            json_ret['summary']['statusCode'] = 200
            json_ret['summary']['msg'] = f'获取数据成功'

            if send_success_count != 0:
                json_ret['summary']['msg'] = f'获取数据成功，并推送数据到：{socket_addr}:{socket_port}/{socket_protocol} 成功'

            json_ret['data']['count'] = len(res_data)

            json_ret['data']['request_api_fail_count'] = request_api_fail_count
            json_ret['data']['not_user_id_count'] = not_user_id_count
            json_ret['data']['send_success_count'] = send_success_count

            json_ret['data']['data_info'] = res_data
        else:
            json_ret['summary']['statusCode'] = first_resp.status_code
            json_ret['summary']['msg'] = f'请求接口：{url} 未成功：{first_resp.text}'

    except Exception as e:
        json_ret['code'] = 500
        json_ret['msg'] = '动作运行失败'
        json_ret['summary']['statusCode'] = 500
        json_ret['summary']['err_msg_lines'] = f'{e.__traceback__.tb_lineno}'
        json_ret['summary']['msg'] = f'{traceback.format_exc()}'
    finally:
        if setSock is not None:
            setSock.close()
            json_ret['summary']['msg'] = json_ret['summary']['msg'] + '\n' + f'关闭SOCK连接成功'
        return json_ret


def get_userid(params, assets, context_info):
    """
    动作：基于手机获取userid
    """
    json_ret = {"code": 200, "msg": "动作运行正常", "summary": {"statusCode": 404, "msg": "动作逻辑执行异常"}, "data": {}}

    corp_id = assets["corp_id"]
    corp_secret = assets["corp_secret"]

    post_data = {
        "mobile": params['mobile_number']
    }
    try:
        access_token = Get_Token(corp_id, corp_secret)
        # end_point = f"https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={access_token}&userid={user_id}"
        end_point = f"https://qyapi.weixin.qq.com/cgi-bin/user/getuserid?access_token={access_token}"

        post_resp = requests.post(end_point, data=json.dumps(post_data), timeout=assets['conn_time_out'])
        user_data_json = json.loads(post_resp.text)
        json_ret['data'] = user_data_json

        if post_resp.status_code == 200 and int(user_data_json['errcode']) == 0:
            json_ret['summary']['statusCode'] = 200
            json_ret['summary']['msg'] = '获取用户信息成功'
        else:
            json_ret['summary']['statusCode'] = int(user_data_json['errcode'])
            json_ret['summary']['msg'] = '获取用户信息失败'

        json_ret['data']['mobile_number'] = params['mobile_number']

    except Exception as e:
        json_ret['code'] = 500
        json_ret['msg'] = '动作运行失败'
        json_ret['summary']['statusCode'] = 500
        json_ret['summary']['err_msg_lines'] = f'{e.__traceback__.tb_lineno}'
        json_ret['summary']['msg'] = f'{traceback.format_exc()}'
    finally:
        return json_ret


# def get_user_info(params, assets, context_info):
#     """
#     开发者：wuk 开发时间戳：1693461505
#     获取用户信息
#     :param 变量名称: str 入参注解
#     :return: 出参注解
#     """
#     corp_id = assets["corp_id"]
#     corp_secret = assets["corp_secret"]
#     user_id = params['user_id'] if "user_id" in params.keys() and params['user_id'] is not None else None
#     token = Get_Token(corp_id=corp_id, corp_secret=corp_secret)
#     user_info = use_userid_get_user_info(token=token, user_id=user_id)
#     json_ret = {"code": 200, "msg": "异常", "data": user_info}


# if __name__ == '__main__':
#     params = {}
#     assets = {}
#     context_info = {}
#     # # 检查企业微信的token是否正常
#     print(health_check(params, assets, context_info))
#     # # 消息发送
#     print(Send_Message(params, assets, context_info))
