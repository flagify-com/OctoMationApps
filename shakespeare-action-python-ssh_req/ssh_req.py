# -*- coding: utf-8 -*-
from app_sdk.sshTools import SSH

def ssh_execute(params, assets, context_info):
    """ssh请求"""

    # SSH服务器地址，Demo: 127.0.0.1
    host = assets["host"]
    # SSH端口号，Demo: 22
    port = assets["port"]
    # SSH用户名
    username = assets["username"]
    # SSH密码
    password = assets["password"]
    # SSH命令，多个用逗号分隔，Demo: ls,pwd
    cmd = params["cmd"]
    # 命令返回后的判断是否执行成功的标志，Demo: #
    ret_flag = params["ret_flag"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"msg": "", "data": ""}}

    '''添加函数实现
    
    '''
    if cmd.find(",") > -1:
        cmd = cmd.split(",")
    elif cmd.find("，") > -1:
        cmd = cmd.split("，")
    else:
        cmd = [cmd]

    ssh = SSH(host, int(port), username, password)
    ssh_ret = ssh.executing(cmd, str_find=ret_flag)
    
    json_ret['data']['msg'] = ssh_ret['msg']
    json_ret['data']['data'] = ssh_ret['data']
    json_ret['code'] = ssh_ret['code']

    return json_ret 

