# -*- coding: utf-8 -*-

import requests
def add_targets(params, assets, context_info):
    """add_targets"""

    # token
    token = assets["token"]
    # awvs地址，例如：https://192.168.1.1:3443/
    awvs_address = assets["awvs_address"]

    # address
    address = params["address"]

    # description
    description = params["description"]

    # criticality
    criticality = 10 if "criticality" not in params.keys() or params["criticality"] == "" else params["criticality"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"address": "", "description": "", "domain": "", "target_id": ""}}

    '''添加函数实现
    
    '''
    url = f"{awvs_address}/api/v1/targets"
    headers = {
        'X-Auth': f'{token}',
        'Content-type': 'application/json'
    }

    data1 = {
        "address": f"{address}",
        "description": f"{description}",
        "criticality": f"{criticality}"
    }

    try:
        response = requests.post(url=url, headers=headers, json=data1, verify=False)
        
        if response.status_code == 201:
            
            json_info = response.json()
            
            # 将返回的JSON信息记录到返回值的data中
            if 'address' in json_info.keys():
                json_ret['data']['address'] = json_info['address']
            if 'description' in json_info.keys():
                json_ret['data']['description'] = json_info['description']
            if 'domain' in json_info.keys():
                json_ret['data']['domain'] = json_info['domain']
            if 'target_id' in json_info.keys():
                json_ret['data']['target_id'] = json_info['target_id']
            
            
    except Exception as e:
        # 如果查询过程中出现异常，记录错误信息到返回值中
        json_ret['msg'] = str(e)



    return json_ret 

def scan_targets(params, assets, context_info):
    """扫描"""

    # token
    token = assets["token"]
    # awvs地址，例如：https://192.168.1.1:3443/
    awvs_address = assets["awvs_address"]

    # target_id
    target_id = params["target_id"]

    # 扫描类型
    profile_id = params["profile_id"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"profile_id": "", "target_id": "", "ui_session_id": "", "scan_id": ""}}

    '''添加函数实现
    
    '''
    url = f"{awvs_address}api/v1/scans"
    headers = {
        'X-Auth': f'{token}',
        'Content-type': 'application/json'
    }

    data = {
    "target_id":f"{target_id}",
    "profile_id":f"{profile_id}",
    "schedule":
        {
        "disable":False,
        "start_date":None,
        "time_sensitive":False
        }
    }

    try:
        response = requests.post(url=url, headers=headers, json=data, verify=False)
        
        if response.status_code == 201:
            
            json_info = response.json()
            
            # 将返回的JSON信息记录到返回值的data中
            if 'target_id' in json_info.keys():
                json_ret['data']['target_id'] = json_info['target_id']
            if 'scan_id' in json_info.keys():
                json_ret['data']['scan_id'] = json_info['scan_id']
            if 'profile_id' in json_info.keys():
                json_ret['data']['profile_id'] = json_info['profile_id']
            if 'start_date' in json_info.keys():
                json_ret['data']['start_date'] = json_info['start_date']

    except Exception as e:
        # 如果查询过程中出现异常，记录错误信息到返回值中
        json_ret['msg'] = str(e)



    return json_ret 

def scan_id(params, assets, context_info):
    """获取目标扫描的id"""

    # token
    token = assets["token"]
    # awvs地址，例如：https://192.168.1.1:3443/
    awvs_address = assets["awvs_address"]

    # target_id
    target_id = params["target_id"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"target_id": "", "last_scan_id": "", "severity_counts": "", "start_date": "", "threat": ""}}

    '''添加函数实现
    
    '''
    url = f"{awvs_address}api/v1/targets/{target_id}"
    headers = {
        'X-Auth': f'{token}',
        'Content-type': 'application/json'
    }

    try:
        response = requests.get(url=url, headers=headers, verify=False)
        
        if response.status_code == 200:
            
            json_info = response.json()
            
            # 将返回的JSON信息记录到返回值的data中
            if 'target_id' in json_info.keys():
                json_ret['data']['target_id'] = json_info['target_id']
            if 'last_scan_id' in json_info.keys():
                json_ret['data']['last_scan_id'] = json_info['last_scan_id']
            if 'severity_counts' in json_info.keys():
                json_ret['data']['severity_counts'] = json_info['severity_counts']
            if 'start_date' in json_info.keys():
                json_ret['data']['start_date'] = json_info['start_date']
            if 'threat' in json_info.keys():
                json_ret['data']['threat'] = json_info['threat']

    except Exception as e:
        # 如果查询过程中出现异常，记录错误信息到返回值中
        json_ret['msg'] = str(e)
    

    return json_ret 

def get_scan_status(params, assets, context_info):
    """获取单个目标状态"""

    # token
    token = assets["token"]
    # awvs地址，例如：https://192.168.1.1:3443/
    awvs_address = assets["awvs_address"]

    # 扫描ID
    scan_id = params["scan_id"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"target": "", "target_id": "", "status": "", "start_date": "", "severity_counts": "", "profile_name": "", "scan_session_id": ""}}

    '''添加函数实现
    
    '''
    url = f"{awvs_address}api/v1/scans/{scan_id}"
    headers = {
        'X-Auth': f'{token}',
        'Content-type': 'application/json'
    }

    try:
        response = requests.get(url=url, headers=headers, verify=False)
        
        if response.status_code == 200:
            
            json_info = response.json()
            
            # 将返回的JSON信息记录到返回值的data中
            if 'target_id' in json_info.keys():
                json_ret['data']['target_id'] = json_info['target_id']
            if 'target' in json_info.keys():
                json_ret['data']['target'] = json_info['target']
            if 'current_session' in json_info.keys():
                json_ret['data']['current_session'] = json_info['current_session']
            if 'start_date' in json_info.keys():
                json_ret['data']['start_date'] = json_info['start_date']
            if 'start_date' in json_info.keys():
                json_ret['data']['start_date'] = json_info['start_date']
            if 'severity_counts' in json_info.keys():
                json_ret['data']['severity_counts'] = json_info['severity_counts']
            if 'profile_name' in json_info.keys():
                json_ret['data']['profile_name'] = json_info['profile_name']
            if 'scan_session_id' in json_info.keys():
                json_ret['data']['scan_session_id'] = json_info['scan_session_id']

    except Exception as e:
        # 如果查询过程中出现异常，记录错误信息到返回值中
        json_ret['msg'] = str(e)


    return json_ret 

def scan_statistics(params, assets, context_info):
    """单个扫描的概况"""

    # token
    token = assets["token"]
    # awvs地址，例如：https://192.168.1.1:3443/
    awvs_address = assets["awvs_address"]

    # scan_id
    scan_id = params["scan_id"]

    # scan_session_id
    scan_session_id = params["scan_session_id"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"vulns": ""}}

    '''添加函数实现
    
    '''
    url = f"{awvs_address}api/v1/scans/{scan_id}/results/{scan_session_id}/statistics"
    headers = {
        'X-Auth': f'{token}',
        'Content-type': 'application/json'
    }

    try:
        response = requests.get(url=url, headers=headers, verify=False)
        
        if response.status_code == 200:
            
            json_info = response.json()
            
            # 将返回的JSON信息记录到返回值的data中
            if 'scanning_app' in json_info.keys():
                json_ret['data']['scanning_app'] = json_info['scanning_app']

    except Exception as e:
        # 如果查询过程中出现异常，记录错误信息到返回值中
        json_ret['msg'] = str(e)


    return json_ret 

def get_targets_info(params, assets, context_info):
    """获取所有目标的信息"""

    # token
    token = assets["token"]
    # awvs地址，例如：https://192.168.1.1:3443/
    awvs_address = assets["awvs_address"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"targets": ""}}

    '''添加函数实现
    
    '''
    url = f"{awvs_address}api/v1/targets"
    headers = {
        'X-Auth': f'{token}',
        'Content-type': 'application/json'
    }




    try:
        response = requests.get(url=url, headers=headers, verify=False)
        
        if response.status_code == 200:
            
            json_info = response.json()
            output = ""
            for test in json_info['targets']:
                address = test['address']
                target_id = test['target_id']
                description = test['description']
                fqdn = test['fqdn']
                last_scan_date = test['last_scan_date']
                last_scan_id = test['last_scan_id']
                last_scan_session_id = test['last_scan_session_id']
                last_scan_session_status = test['last_scan_session_status']
                severity_counts = test['severity_counts']

                output += f"Address: {address}\n"
                output += f"Target ID: {target_id}\n"
                output += f"Description: {description}\n"
                output += f"FQDN: {fqdn}\n"
                output += f"Last Scan Date: {last_scan_date}\n"
                output += f"Last Scan ID: {last_scan_id}\n"
                output += f"Last Scan Session ID: {last_scan_session_id}\n"
                output += f"Last Scan Session Status: {last_scan_session_status}\n"
                output += f"Severity Counts: {severity_counts}\n"

                output += "----------------------------------------------------------------------------------------------------------------\n"
            
            # 将返回的JSON信息记录到返回值的data中
            
            json_ret['data']['targets'] = output

    except Exception as e:
        # 如果查询过程中出现异常，记录错误信息到返回值中
        json_ret['msg'] = str(e)


    return json_ret 

def delete_targets(params, assets, context_info):
    """删除目标"""

    # token
    token = assets["token"]
    # awvs地址，例如：https://192.168.1.1:3443/
    awvs_address = assets["awvs_address"]

    # target_id
    target_id = params["target_id"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"txt": ""}}

    '''添加函数实现
    
    '''
    url = f"{awvs_address}api/v1/targets/{target_id}"
    headers = {
        'X-Auth': f'{token}',
        'Content-type': 'application/json'
    }

    try:
        response = requests.delete(url=url, headers=headers, verify=False)
        
        if response.status_code == 204:
            
            json_info = "目标已删除"
            
            # 将返回的JSON信息记录到返回值的data中
            
            json_ret['data']['txt'] = json_info

    except Exception as e:
        # 如果查询过程中出现异常，记录错误信息到返回值中
        json_ret['msg'] = str(e)


    return json_ret 

