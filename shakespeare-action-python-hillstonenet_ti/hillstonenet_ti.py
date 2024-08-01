# -*- coding: utf-8 -*-
import json
import requests
import urllib.parse

def health_check(params, assets, context_info):
    """健康检查：Domain"""

    # API域名，默认：ti.hillstonenet.com.cn
    api_domain = "ti.hillstonenet.com.cn" if "api_domain" not in assets.keys() or assets["api_domain"] == "" else assets["api_domain"]
    # 调用API的密钥，客通过官方网站后台获取
    api_key = assets["api_key"]

    domain = "hillstonenet.com"

    # 返回值
    json_ret = {
        "code": 200, 
        "msg": "",
        "data": {"err_code": 0, "err_msg": "", "risk_level": "unreported", "raw_data": {}, "threat_type": []},
        "summary": {"statusCode": 200, "msg": "健康检查成功"}
    }
    url = f'https://{api_domain}/api/domain/reputation?key={domain}'
    headers = {
        'X-Auth-Token':api_key,
        'ACCEPT':'application/json',
        'X-API-Version':'1.0.0',
        'X-API-Language':'en'
    }
    try:
        response = requests.get(url, headers=headers)
        report = response.text.encode('utf-8')
        report_json = json.loads(report)
        response_code = report_json.get("response_code", 100)
        if response_code in (1, 0, -1, -2, -3, -4, -5):
            json_ret["data"]["err_code"] = response_code
            json_ret["data"]["err_msg"] = report_json.get("response_msg", "")
        if response_code == 0 and "data" in report_json.keys():
            if "result" in report_json["data"].keys():
                json_ret["data"]["risk_level"] = report_json["data"]["result"]
            if "threat_type" in report_json["data"].keys():
                json_ret["data"]["threat_type"] = report_json["data"]["threat_type"]
        json_ret["data"]["raw_data"] = report_json
        if response_code == 0:
            json_ret["data"]["summary"] = {"statusCode": 200, "msg": "健康检查成功"}
        else:
            json_ret["data"]["summary"] = {"statusCode": response_code, "msg": "健康检查失败"}
    except Exception as e:
        json_ret["data"]["err_code"] = 500
        json_ret["data"]["err_msg"] = str(e)
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = "健康检查失败"

    return json_ret 

def detail_file(params, assets, context_info):
    """高级威胁查询：File"""

    # API域名，默认：ti.hillstonenet.com.cn
    api_domain = "ti.hillstonenet.com.cn" if "api_domain" not in assets.keys() or assets["api_domain"] == "" else assets["api_domain"]
    # 调用API的密钥，客通过官方网站后台获取
    api_key = assets["api_key"]

    file_hash = params["file_hash"]

    # 返回值
    json_ret = {
        "code": 200, 
        "msg": "",
        "data": {
            "err_code": 0, 
            "err_msg": "", 
            "risk_level": "", 
            "threat_type": [], 
            "raw_data": {
                "data": {
                    "result": "noreported",
                    "sha256": "",
                    "sha1": "",
                    "md5": "",
                    "tags": [],
                    "threat_type": [],
                    "basic_info": {
                        "file_size": 0,
                        "file_type": "",
                        "first_seen": 0,
                        "last_seen": 0,
                        "scan_date": 0
                    },
                    "connect_ips": [],
                    "download_ips": [],
                    "referer_ips": [],
                    "connect_domains": [],
                    "download_domains": [],
                    "referer_domains": []
                },
                "response_code": 0,
                "response_msg": ""
            }
        }
    }

    url = f'https://{api_domain}/api/file/detail?key={file_hash}'
    headers = {
        'X-Auth-Token':api_key,
        'ACCEPT':'application/json',
        'X-API-Version':'1.0.0',
        'X-API-Language':'en'
    }
    try:
        response = requests.get(url, headers=headers)
        report = response.text.encode('utf-8')
        report_json = json.loads(report)
        response_code = report_json.get("response_code", 100)
        if response_code in (1, 0, -1, -2, -3, -4, -5):
            json_ret["data"]["err_code"] = response_code
            json_ret["data"]["err_msg"] = report_json.get("response_msg", "")
        if response_code == 0 and "data" in report_json.keys():
            if "result" in report_json["data"].keys():
                json_ret["data"]["risk_level"] = report_json["data"]["result"]
            if "threat_type" in report_json["data"].keys():
                json_ret["data"]["threat_type"] = report_json["data"]["threat_type"]
        json_ret["data"]["raw_data"] = report_json
    except Exception as e:
        json_ret["data"]["err_code"] = 500
        json_ret["data"]["err_msg"] = str(e)

    return json_ret

def detail_url(params, assets, context_info):
    """高级威胁查询：URL"""

    # API域名，默认：ti.hillstonenet.com.cn
    api_domain = "ti.hillstonenet.com.cn" if "api_domain" not in assets.keys() or assets["api_domain"] == "" else assets["api_domain"]
    # 调用API的密钥，客通过官方网站后台获取
    api_key = assets["api_key"]

    url = params["url"]
    parsed_url = urllib.parse.urlparse(url)
    url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # 返回值
    json_ret = {
        "code": 200, 
        "msg": "",
        "data": {
            "err_code": 0, 
            "err_msg": "", 
            "risk_level": "", 
            "threat_type": [], 
            "raw_data": {
                "data": {
                    "result": "noreported",
                    "url": "",
                    "hash_sha256": "",
                    "related_ips": [],
                    "related_domains": [],
                    "related_files": []
                },
                "response_code": 0,
                "response_msg": "OK"
            }
        }
    }

    url = f'https://{api_domain}/api/url/detail?key={url}'
    headers = {
        'X-Auth-Token':api_key,
        'ACCEPT':'application/json',
        'X-API-Version':'1.0.0',
        'X-API-Language':'en'
    }
    try:
        response = requests.get(url, headers=headers)
        report = response.text.encode('utf-8')
        report_json = json.loads(report)
        response_code = report_json.get("response_code", 100)
        if response_code in (1, 0, -1, -2, -3, -4, -5):
            json_ret["data"]["err_code"] = response_code
            json_ret["data"]["err_msg"] = report_json.get("response_msg", "")
        if response_code == 0 and "data" in report_json.keys():
            if "result" in report_json["data"].keys():
                json_ret["data"]["risk_level"] = report_json["data"]["result"]
            if "threat_type" in report_json["data"].keys():
                json_ret["data"]["threat_type"] = report_json["data"]["threat_type"]
        json_ret["data"]["raw_data"] = report_json
    except Exception as e:
        json_ret["data"]["err_code"] = 500
        json_ret["data"]["err_msg"] = str(e)

    return json_ret

def detail_domain(params, assets, context_info):
    """高级威胁查询：Domain"""

    # API域名，默认：ti.hillstonenet.com.cn
    api_domain = "ti.hillstonenet.com.cn" if "api_domain" not in assets.keys() or assets["api_domain"] == "" else assets["api_domain"]
    # 调用API的密钥，客通过官方网站后台获取
    api_key = assets["api_key"]

    domain = params["domain"]

    # 返回值
    json_ret = {
        "code": 200, 
        "msg": "",
        "data": {
            "err_code": 0, 
            "err_msg": "", 
            "risk_level": "", 
            "threat_type": [], 
            "raw_data": {
                "data": {
                    "result": "unreported",
                    "domain_name": "",
                    "current_whois": "",
                    "dns_records": [],
                    "current_ips": [],
                    "history_ips": [],
                    "sub_domains": [],
                    "domain_siblings": [],
                    "download_files": [],
                    "referer_files": [],
                    "connect_files": []
                },
                "response_code": 0,
                "response_msg": ""
            }
        }
    }

    url = f'https://{api_domain}/api/domain/detail'
    headers = {
        'X-Auth-Token':api_key,
        'ACCEPT':'application/json',
        'X-API-Version':'1.0.0',
        'X-API-Language':'en'
    }
    params = {
        "key": domain
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        report = response.text.encode('utf-8')
        report_json = json.loads(report)
        response_code = report_json.get("response_code", 100)
        if response_code in (1, 0, -1, -2, -3, -4, -5):
            json_ret["data"]["err_code"] = response_code
            json_ret["data"]["err_msg"] = report_json.get("response_msg", "")
        if response_code == 0 and "data" in report_json.keys():
            if "result" in report_json["data"].keys():
                json_ret["data"]["risk_level"] = report_json["data"]["result"]
            if "threat_type" in report_json["data"].keys():
                json_ret["data"]["threat_type"] = report_json["data"]["threat_type"]
        json_ret["data"]["raw_data"] = report_json
    except Exception as e:
        json_ret["data"]["err_code"] = 500
        json_ret["data"]["err_msg"] = str(e)

    return json_ret

def detail_ip(params, assets, context_info):
    """高级威胁查询：IP"""

    # API域名，默认：ti.hillstonenet.com.cn
    api_domain = "ti.hillstonenet.com.cn" if "api_domain" not in assets.keys() or assets["api_domain"] == "" else assets["api_domain"]
    # 调用API的密钥，客通过官方网站后台获取
    api_key = assets["api_key"]

    # 待查询的IP地址
    ip = params["ip"]

    # 返回值
    json_ret = {
        "code": 200, 
        "msg": "",
        "data": {
            "err_code": 0, 
            "err_msg": "", 
            "risk_level": "", 
            "threat_type": [], 
            "raw_data": {
                "data": {
                    "result": "unreported",
                    "tags": [],
                    "ports": [],
                    "threat_type": [],
                    "ip_address": "",
                    "basic_info": {
                        "network": "",
                        "carrier": "",
                        "location": {
                            "country": "",
                            "province": "",
                            "city": "",
                            "longitude": 0,
                            "latitude": 0,
                            "country_code": ""
                        }
                    },
                    "rdns_list": [],
                    "current_domains": [],
                    "history_domains": [],
                    "download_files": [],
                    "referer_files": [],
                    "connect_files": []
                },
                "response_code": 0,
                "response_msg": ""
            }
        }
    }

    url = f'https://{api_domain}/api/ip/detail?key={ip}'
    headers = {
        'X-Auth-Token':api_key,
        'ACCEPT':'application/json',
        'X-API-Version':'1.0.0',
        'X-API-Language':'en'
    }
    try:
        response = requests.get(url, headers=headers)
        report = response.text.encode('utf-8')
        report_json = json.loads(report)
        response_code = report_json.get("response_code", 100)
        if response_code in (1, 0, -1, -2, -3, -4, -5):
            json_ret["data"]["err_code"] = response_code
            json_ret["data"]["err_msg"] = report_json.get("response_msg", "")
        if response_code == 0 and "data" in report_json.keys():
            if "result" in report_json["data"].keys():
                json_ret["data"]["risk_level"] = report_json["data"]["result"]
            if "threat_type" in report_json["data"].keys():
                json_ret["data"]["threat_type"] = report_json["data"]["threat_type"]
        json_ret["data"]["raw_data"] = report_json
    except Exception as e:
        json_ret["data"]["err_code"] = 500
        json_ret["data"]["err_msg"] = str(e)

    return json_ret