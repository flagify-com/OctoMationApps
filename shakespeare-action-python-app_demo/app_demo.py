# -*- coding: utf-8 -*-
import requests
import os

def rand_qinghua(params, assets, context_info):
    """随机输出土味情话"""

    # http超时参数，默认5s
    timeout = 5 if "timeout" not in assets.keys() or assets["timeout"] == "" else assets["timeout"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"content": "", "msg": ""}}

    try:
        url = "https://api.uomg.com/api/rand.qinghua?format=json"
        resp_json = requests.get(url,timeout=timeout).json()
        json_ret["data"] = resp_json

    except Exception as e:
        msg = str(e)
        # 服务异常时，设置 summery.statusCode != 200
        json_ret = {"code": 200, "msg": msg, "data": {"content": "", "msg": msg},"sumarry":{"statusCode":400}}

    return json_ret 


def read_file(params, assets, context_info):
    """读取文件内容（小文件）"""

    # 从参数传入的文件，上传后的文件会重命名.例：/opt/shakespeare/data/app_files/action_local/e478ec27-9bde-4592-a15b-77e857c7d416/badb5150-cdf3-4e7a-b4eb-67f8bc45a967/68d5db3525da45efb4503b07a18c8f45.zip
    file_path = params["file"]

    json_ret = {"code": 200, "msg": "","data": {"content": "","msg":"ok"}}

    # 获取文件大小（以字节为单位）
    file_size_bytes = os.path.getsize(file_path)

    # 定义0.5MB的字节数
    half_megabyte = 0.5 * 1024 * 1024  # 1 MB = 1024 KB, 1 KB = 1024 bytes

    # 检查文件大小是否小于0.5MB
    if file_size_bytes < half_megabyte:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            json_ret["data"]["content"] = f.read()

    else:
        json_ret["data"]["msg"] = "The file is 0.5MB or larger."

    return json_ret 