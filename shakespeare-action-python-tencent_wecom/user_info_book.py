import json
import requests
import os
from sqlite_control import *

'''
这个文件负责通讯录类方法
'''
# 缓冲文件地址
user_file_path = "/opt/shakespeare/data/work_wechat"
if not os.path.exists(user_file_path):
    os.mkdir(user_file_path)


def get_user_id_list(token):
    """
    开发者：wuk 开发时间戳：1693460550
    获取用户ID列表
    :param 变量名称: str 入参注解
    :return: 出参注解
    """
    api_url = f"https://qyapi.weixin.qq.com/cgi-bin/user/list_id?access_token={token}"
    user_id_list = []
    res_json = None
    data = {
        "limit": 10000
    }
    while res_json != None and "next_cursor" not in res_json.keys():
        res = requests.post(url=api_url, data=json.dumps(data))
        res_json = json.loads(res.text)
        if res_json['errmsg'] != "ok":
            return res_json
        elif "next_cursor" in res_json.keys():
            data['cursor'] = res_json['next_cursor']
        user_id_list += res_json['dept_user']
    return user_id_list


def use_userid_get_user_info(token, user_id, time_out=5) -> dict:
    """
    开发者：wuk 开发时间戳：1693460785
    使用userid获取用户信息
    :param token: str token
    :param user_id: str 用户id
    :param corp_id: str 企业id
    :return: dict
    """
    api_url = f"https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={token}&userid={user_id}"
    res = requests.get(api_url, timeout=time_out)
    user_data_json = json.loads(res.text)
    return user_data_json


def update_user_info_db(token, corp_id=None):
    """
    开发者：wuk 开发时间戳：1693461981
    更新人员数据库
    :param 变量名称: str 入参注解
    :return: 出参注解
    """
    db_path = f"{user_file_path}/token_info_{corp_id}.db"
    if not os.path.exists(db_path):
        # 数据库不存在，需要创建数据库
        create_table_sql = "CREATE TABLE user_info(" \
                           "open_userid CHAR(50) PRIMARY KEY," \
                           "user_id CHAR(50) NOT NULL," \
                           "user_name CHAR(50) NOT NULL," \
                           "dep_id cher(50) NOT NULL," \
                           "mobile cher(50)," \
                           "email cher(50)," \
                           "biz_mail cher(50)," \
                           ");"
        conn_db = sqlite(db_path)
        conn_db.get_sql(create_table_sql)
    else:
        conn_db = sqlite(db_path)
    user_id_list = get_user_id_list(token=token)
    if not isinstance(user_id_list, list):
        conn_db.close()
        raise RuntimeError(f"运行异常：{user_id_list}")
    user_all_info_list = []
    for user_dep_id in user_id_list:
        user_id = user_dep_id['userid']
        user_info = user_all_info_list(token, user_id)
        if user_info['errmsg'] == "ok":
            user_all_info_list.append(user_info)
    api_url = f"https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={token}&userid={user_id}"
    res = requests.get(api_url)
    user_data_json = json.loads(res)
    raise RuntimeError("运行异常：调用请勿填写corp_id参数")
    return user_data_json
