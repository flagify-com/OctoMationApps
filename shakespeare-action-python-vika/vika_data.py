# -*- coding: utf-8 -*-
# dingbaolin
import json
from urllib.parse import urljoin

import requests
requests.packages.urllib3.disable_warnings()


def is_valid_json(my_str):
    try:

        # 删除字段使用：如果需要清空某字段的值，可设置为 null。例如 "状态": null 将清除该记录对应的「状态」列的值。
        if my_str is None:
            return None
        # 如果是列表或字典，直接返回
        if isinstance(my_str, list) or isinstance(my_str, dict):
            return my_str

        json.loads(my_str)
        return json.loads(my_str)
    except json.JSONDecodeError:
        return my_str


class VIKA:

    def __init__(self, assets,context_info=None):

        self.host = assets['host']
        self.datasheetId = assets['datasheetId']
        self.space_id = assets['space_id']
        self.header = {
            "Authorization": "Bearer " + assets['api_token'],
            "Content-Type": "application/json",
            "X-Space-Id": self.space_id
        }

    def send_request(self, method, uri, param=None, data=None):

        full_url = urljoin(self.host, uri)
        ret = None
        if method.upper() == "GET":
            try:
                ret = requests.get(full_url, headers=self.header, params=param, timeout=8)
            except requests.exceptions.Timeout:
                ret = requests.get(full_url, headers=self.header, params=param, timeout=8)
        elif method.upper() == "POST":
            ret = requests.post(full_url, headers=self.header, json=data)
        elif method.upper() == "PATCH":
            ret = requests.patch(full_url, headers=self.header, json=data)

        return ret.json()

    def spaces(self):
        # 获取字段
        uri = '/fusion/v1/spaces'
        ret = self.send_request('get', uri)
        return ret

    def get_records(self, filter_by_formula, fields=None):
        # 获取字段
        uri = f'/fusion/v1/datasheets/{self.datasheetId}/records'
        param = {'pageSize': 1000}
        if filter_by_formula:
            param["filterByFormula"] = filter_by_formula
        if fields:
            param['fields'] = fields
        ret = self.send_request('get', uri, param=param)
        print(ret)
        return ret

    def patch_records(self, record_id, col_name, value):

        uri = f'/fusion/v1/datasheets/{self.datasheetId}/records'

        data = {
            "records": [
                {
                    "recordId": record_id,
                    "fields": {
                        # 将value字符串可以转换成json的进行转换
                        col_name: is_valid_json(value)
                        # "SOAR处理结果": "已封禁"
                    }
                }
            ],
            "fieldKey": "name"
        }

        ret = self.send_request('patch', uri, data=data)
        return ret

    def get_fields(self):

        uri = f'/fusion/v1/datasheets/{self.datasheetId}/fields'
        ret = self.send_request('get', uri)
        return ret


def spaces(params, assets, context_info):
    # 获取空间站列表
    json_ret = {"code": 200, "msg": "请求成功"}

    try:
        vika = VIKA(assets)
        json_ret = vika.spaces()

    except requests.exceptions.ConnectionError:
        json_ret['code'] = 500
        json_ret['msg'] = "连接异常，请检查url或网络是否可达"
    except Exception as e:
        json_ret['code'] = 500
        json_ret['msg'] = f"其他错误{e}"

    return json_ret


def search_tables(params, assets, context_info):
    json_ret = {"code": 200, "msg": "请求成功", "data": {}}

    filter_by_formula = params.get('filter_by_formula')

    vika = VIKA(assets)

    ret = vika.get_records(filter_by_formula)
    if ret['message'] == "api_param_formula_error":
        # logger.info('filter_by_formula参数错误')
        json_ret['code'] = 400
        json_ret['msg'] = "filter_by_formula参数错误"
        return json_ret

    json_ret['data'] = ret['data']
    return json_ret


def change_tables(params, assets, context_info):
    json_ret = {"code": 200, "msg": "请求成功", "data": {}}

    try:
        record_id = params['recordId']
        col_name = params['col_name']
        value = params['value']
    except KeyError as e:
        json_ret['code'] = 400
        json_ret['msg'] = f"缺失必要参数{e}"
        return json_ret

    vika = VIKA(assets)
    col_ret = vika.patch_records(record_id=record_id, col_name=col_name, value=value)

    json_ret['msg'] = col_ret['message']
    json_ret['data'] = col_ret
    return json_ret
