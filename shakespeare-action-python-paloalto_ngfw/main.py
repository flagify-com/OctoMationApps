# -*- coding: utf-8 -*-


def blockIP(params, assets, context_info):
    """封禁 IP"""

    # 防火墙地址，格式为 http[s]://IP地址或域名:port
    url = assets["url"]
    # 有访问防火墙 API 权限的 API Key，参考使用说明
    api_key = assets["api_key"]

    #  需要封禁的 IP
    ip = params["ip"]

    # 创建动态地址组时的 IP 标签，将 IP 打上该标签后会自动添加到创建动态地址，防火墙策略会应用该创建动态地址，自动封禁 IP
    ip_tag = params["ip_tag"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"result":""}}


    action: str = "register"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    xml_template = """<uid-message><type>update</type><payload><{action}>{entries}</{action}></payload></uid-message>"""
    entries = f'<entry ip="{ip}"><tag><member>{ip_tag}</member></tag></entry>'
    cmd = urllib.parse.quote(xml_template.format(action=action, entries=entries))
    action_url = f"{url}/api/?type=user-id&key={api_key}&cmd={cmd}"
    res = requests.post(action_url, verify=False, headers=headers)
    if res.status_code != 200:
        msg = ""
        res_xml = res.text
        searched_msg = re.search("<msg>(.*)</msg>", res_xml)
        if searched_msg:
            msg = searched_msg[0][5:-6]
        json_ret['data']['result'] = f"PAFW 封禁 IP 失败 {res.status_code}{f' {msg}' if msg else ''}"

    return json_ret 

