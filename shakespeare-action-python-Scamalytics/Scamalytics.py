# -*- coding: utf-8 -*-
import json
import bs4
import requests

def get_ip_fraud_risk_info(params, assets, context_info):
    """获取IP威胁信息"""
    api_user = assets.get("api_user", "")
    api_key = assets.get("api_key", "")
    ip = params.get("ip", "")
    #/very high/high/medium/low
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "method": "",
            "err_code": 0,
            "err_msg": "",
            "ip": "",
            "hostname": "",
            "score": -1,
            "risk": "low",
            "anonymizing_vpn": False,
            "tor": False,
            "server": False,
            "public_proxy": False,
            "web_proxy": False,
            "search_engine_robot": False,
            "ip_country_code": "",
            "ip_country_name": "",
            "ip_state_name": "",
            "ip_city": "",
            "ip_district": "",
            "ip_postcode": "",
            "ip_geolocation": "",
            "ip_geolocation_longtitude": 0,
            "ip_geolocation_latitude": 0,
            "proxy_type": "0",
            "connection_type": "",
            "as_number": "",
            "isp_name": "",
            "isp_fraud_score": -1,
            "organization_name": "",
            "url": "",
            "exec": "",
            "credits": {
                "credits_used": 0,
                "credits_remaining": 0,
                "last_sync_timestamp_utc": "",
                "seconds_elapsed_since_last_sync": 0,
                "note": ""
            },
            "raw_data": {}
        }
    }
    if ip == "":
        json_ret["data"]["err_code"] = 400
        json_ret["data"]["err_msg"] = "IP不能为空"
        return json_ret
    if api_key and api_user:
        json_ret["data"]["method"] = "api"
        url = f"https://api11.scamalytics.com/{api_user}/?key={api_key}&ip={ip}"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                json_response= response.json()
                json_ret["data"]["raw_data"] = json_response
                if 'status' in json_response.keys() and json_response['status'] == 'ok':
                    json_ret["data"]["ip"] = json_response.get('ip', ip)
                    json_ret["data"]["score"] = json_response.get('score', -1)
                    json_ret["data"]["risk"] = json_response.get('risk', '-')
                    json_ret["data"]["hostname"] = json_response.get('hostname', '-')
                    json_ret["data"]["ip_country_code"] = json_response.get('ip_country_code', '')
                    json_ret["data"]["ip_state_name"] = json_response.get('ip_state_name', '')
                    json_ret["data"]["ip_city"] = json_response.get('ip_city', '')
                    json_ret["data"]["ip_postcode"] = json_response.get('ip_postcode', '')
                    json_ret["data"]["ip_geolocation"] = json_response.get('ip_geolocation', '')
                    if json_ret["data"]["ip_geolocation"] != '' and ',' in json_ret["data"]["ip_geolocation"]:
                        # 从输出结果中分隔出经度和纬度
                        longtitude, latitude = json_ret["data"]["ip_geolocation"].split(',')
                        json_ret["data"]["ip_geolocation_longtitude"] = float(longtitude)
                        json_ret["data"]["ip_geolocation_latitude"] = float(latitude)
                    json_ret["data"]["ip_country_name"] = json_response.get('ip_country_name', '')
                    json_ret["data"]["connection_type"] = json_response.get('connection_type', '')
                    json_ret["data"]["as_number"] = json_response.get('as_number', '')
                    json_ret["data"]["isp_name"] = json_response.get('ISP Name', '')
                    isp_fraud_score = json_response.get('ISP Fraud Score', -1)
                    json_ret["data"]["isp_fraud_score"] = float(isp_fraud_score)
                    json_ret["data"]["organization_name"] = json_response.get('Organization Name', '')
                    json_ret["data"]["url"] = json_response.get('url', '')
                    json_ret["data"]["exec"] = json_response.get('exec', '')
                    if "credits" in json_response.keys():
                        json_ret["data"]["credits"]["used"] = json_response.get('credits_used', 0)
                        json_ret["data"]["credits"]["remaining"] = json_response.get('credits_remaining', 0)
                        json_ret["data"]["credits"]["last_sync_timestamp_utc"] = json_response.get('last_sync_timestamp_utc', '')
                        json_ret["data"]["credits"]["seconds_elapsed_since_last_sync"] = json_response.get('seconds_elapsed_since_last_sync', 0)
                        json_ret["data"]["credits"]["note"] = json_response.get('note', '')
                    
                    json_ret["data"]["proxy_type"] = json_response.get('proxy_type', '')
                    if json_ret["data"]["proxy_type"].upper() == "VPN":
                        json_ret["data"]["anonymizing_vpn"] = True
                    elif json_ret["data"]["proxy_type"].upper() == "PUB":
                        json_ret["data"]["public_proxy"] = True
                    elif json_ret["data"]["proxy_type"].upper() == "WEB":
                        json_ret["data"]["web_proxy"] = True
                    elif json_ret["data"]["proxy_type"].upper() == "SES":
                        json_ret["data"]["search_engine_robot"] = True
                    elif json_ret["data"]["proxy_type"].upper() == "TOR":
                        json_ret["data"]["tor"] = True
                    elif json_ret["data"]["proxy_type"].upper() == "DCH":
                        json_ret["data"]["server"] = True

                    json_ret["data"]["err_code"] = 0
                    json_ret["data"]["err_msg"] = json_response['status']
                else:
                    json_ret["data"]["err_code"] = 500
                    json_ret["data"]["err_msg"] = response.text
            else:
                json_ret["data"]["err_code"] = response.status_code
                json_ret["data"]["err_msg"] = response.text
        except Exception as e:
            json_ret["data"]["err_code"] = 500
            json_ret["data"]["err_msg"] = str(e)
    else:
        return get_ip_fraud_risk_info_from_web(params, assets, None)
    return json_ret
    x = {
        "status": "ok",
        "mode": "live",
        "ip": "216.58.194.174",
        "score": 5,
        "risk": "low",
        "url": "https://scamalytics.com/ip/216.58.194.174",
        "exec": "3.54 ms",
        "credits": {
            "used": 1,
            "remaining": 49999,
            "last_sync_timestamp_utc": "2024-07-30 11:58:04",
            "seconds_elapsed_since_last_sync": 32,
            "note": "Credits used and remaining are approximate values."
        },
        "ISP Name": "Google LLC",
        "ISP Fraud Score": "8",
        "Organization Name": "Google LLC",
        "ip_country_code": "US",
        "ip_state_name": "Arizona",
        "ip_city": "Phoenix",
        "ip_postcode": "85001",
        "ip_geolocation": "33.4484,-112.074",
        "ip_country_name": "United States",
        "proxy_type": "PUB",
        "connection_type": "",
        "as_number": "15169"
    }


def search_ip(params, assets, contex_info):
    """保留老函数，兼容旧版本"""
    return get_ip_fraud_risk_info(params, assets, contex_info)

def get_ip_fraud_risk_info_from_web(params, assets, context_info):
    """通过web方式获取IP威胁信息"""
    ip = params.get("ip", "")
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "method": "web",
            "err_code": 0,
            "err_msg": "",
            "ip": "",
            "hostname": "",
            "score": -1,
            "risk": "low",
            "anonymizing_vpn": False,
            "tor": False,
            "server": False,
            "public_proxy": False,
            "web_proxy": False,
            "search_engine_robot": False,
            "ip_country_code": "",
            "ip_state_name": "",
            "ip_city": "",
            "ip_district": "",
            "ip_postcode": "",
            "ip_geolocation": "",
            "ip_geolocation_longtitude": 0,
            "ip_geolocation_latitude": 0,
            "proxy_type": "0",
            "connection_type": "",
            "as_number": "",
            "isp_name": "",
            "isp_fraud_score": -1,
            "organization_name": "",
            "url": "",
            "exec": "",
            "credits": {
                "credits_used": 0,
                "credits_remaining": 0,
                "last_sync_timestamp_utc": "",
                "seconds_elapsed_since_last_sync": 0,
                "note": ""
            },
            "raw_data": {}
        }
    }

    if ip == "":
        json_ret["data"]["err_code"] = 400
        json_ret["data"]["err_msg"] = "IP不能为空"
        return json_ret

    url = 'https://scamalytics.com/ip/{0}'.format(ip)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
    try:
        response = requests.get(url, headers={'User-Agent': user_agent}, timeout=30)
        if response.status_code == 200:
            if "is a private IP address" in response.text:
                json_ret["data"]["err_msg"] = "私有IP地址"
                json_ret["data"]["isp_name"] = "Private network"
                return json_ret
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all(['th', 'td'])
                    if len(cols) == 2:
                        key = cols[0].get_text(strip=True)
                        value = cols[1].get_text(strip=True)
                        if key == "Hostname":
                            if value != "" and value != "n/a":
                                json_ret["data"]["hostname"] = value
                        elif key == "ASN":
                            if value != "" and value != "n/a":
                                json_ret["data"]["as_number"] = value
                        elif key == "ISP Name":
                            if value != "" and value != "n/a":
                                json_ret["data"]["isp_name"] = value
                        elif key == "Organization Name":
                            if value != "" and value != "n/a":
                                json_ret["data"]["organization_name"] = value
                        elif key == "Connection type":
                            if value != "" and value != "n/a":
                                json_ret["data"]["connection_type"] = value
                        elif key == "Country Name":
                            if value != "" and value != "n/a":
                                json_ret["data"]["ip_country_name"] = value
                        elif key == "Country Code":
                            if value != "" and value != "n/a":
                                json_ret["data"]["ip_country_code"] = value
                        elif key == "State / Province":
                            if value != "" and value != "n/a":
                                json_ret["data"]["ip_state_name"] = value
                        elif key == "District / County":
                            if value != "" and value != "n/a":
                                json_ret["data"]["ip_district"] = value
                        elif key == "City":
                            if value != "" and value != "n/a":
                                json_ret["data"]["ip_city"] = value
                        elif key == "Postal Code":
                            if value != "" and value != "n/a":
                                json_ret["data"]["ip_postcode"] = value
                        elif key == "Longitude":
                            if value != "" and value != "n/a":
                                try:
                                    json_ret["data"]["ip_geolocation_longtitude"] = float(value)
                                except:
                                    pass
                        elif key == "Latitude":
                            if value != "" and value != "n/a":
                                try:
                                    json_ret["data"]["ip_geolocation_latitude"] = float(value)
                                except:
                                    pass
                        elif key == "Anonymizing VPN":
                            if value == 'Yes':
                                json_ret["data"]["anonymizing_vpn"] = True
                                json_ret["data"]["proxy_type"] = "VPN"
                        elif key == "Tor Exit Node":
                            if value == 'Yes':
                                json_ret["data"]["tor"] = True
                                json_ret["data"]["proxy_type"] = "TOR"
                        elif key == "Server":
                            if value == 'Yes':
                                json_ret["data"]["server"] = True
                                json_ret["data"]["proxy_type"] = "DCH"
                        elif key == "Public Proxy":
                            if value == 'Yes':
                                json_ret["data"]["public_proxy"] = True
                                json_ret["data"]["proxy_type"] = "PUB"
                        elif key == "Web Proxy":
                            if value == 'Yes':
                                json_ret["data"]["web_proxy"] = True
                                json_ret["data"]["proxy_type"] = "WEB"
                        elif key == "Search Engine Robot":
                            if value == 'Yes':
                                json_ret["data"]["search_engine_robot"] = True
                                json_ret["data"]["proxy_type"] = "SES"
            
            if json_ret["data"]["ip_geolocation_longtitude"] != 0 and json_ret["data"]["ip_geolocation_latitude"] != 0:
                json_ret["data"]["ip_geolocation"] = "{0},{1}".format(json_ret["data"]["ip_geolocation_longtitude"], json_ret["data"]["ip_geolocation_latitude"])
            
            json_ret["data"]["ip"] = ip
            json_ret["data"]["url"] = f"https://scamalytics.com/ip/{ip}"

            pre = soup.find('pre')
            if pre:
                try:
                    json_pre = json.loads(pre.get_text(strip=True))
                    if "ip" in json_pre.keys():
                        json_ret["data"]["ip"] = json_pre["ip"]
                    if "score" in json_pre.keys():
                        json_ret["data"]["score"] = int(json_pre["score"])
                    if "risk" in json_pre.keys():
                        json_ret["data"]["risk"] = json_pre["risk"]
                except Exception as e:
                    json_ret["data"]["err_code"] = 500
                    json_ret["data"]["err_msg"] = str(e)
        else:
            json_ret["data"]["err_code"] = response.status_code
            json_ret["data"]["err_msg"] = response.text
    except Exception as e:
        json_ret["data"]["err_code"] = 500
        json_ret["data"]["err_msg"] = str(e)
    return json_ret


def health_check(params, assets, context_info):
    """健康检查"""
    api_user = assets.get("api_user", "")
    api_key = assets.get("api_key", "")
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "err_code": 0,
            "err_msg": "",
            "method": "",
            "raw_data": {}
        },
        "summary":{
            "statusCode": 200,
            "msg": ""
        }
    }
    if api_user and api_key:
        json_ret["data"]["method"] = "api"
        url = f"https://api11.scamalytics.com/{api_user}/?key={api_key}&ip=8.8.8.8&test=1"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                json_response = response.json()
                if "status" in json_response.keys() and json_response['status'] == 'ok':
                    json_ret["data"]["raw_data"] = json_response
                    json_ret["summary"]["msg"] = "API方式查询，健康检查成功"
                else:
                    json_ret["data"]["err_code"] = 500
                    json_ret["data"]["err_msg"] = "API接口返回内容不符合要求，请查看原始数据"
                    json_ret["summary"]["statusCode"] = 521
                    json_ret["summary"]["msg"] = "API方式查询，健康检查失败"
            else:
                json_ret["data"]["err_code"] = response.status_code
                json_ret["data"]["err_msg"] = response.text
                json_ret["summary"]["statusCode"] = 522
                json_ret["summary"]["msg"] = "API方式查询，健康检查失败"
        except Exception as e:
            json_ret["data"]["err_code"] = 500
            json_ret["data"]["err_msg"] = str(e)
            json_ret["summary"]["statusCode"] = 523
            json_ret["summary"]["msg"] = "API方式查询，健康检查失败"
    else:
        json_ret["data"]["method"] = "web"
        url = 'https://scamalytics.com/ip/8.8.8.8'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
        try:
            response = requests.get(url, headers={'User-Agent': user_agent}, timeout=30)
            if response.status_code == 200:
                soup = bs4.BeautifulSoup(response.content, 'html.parser')
                pre = soup.find('pre')
                if pre:
                    try:
                        json_pre = json.loads(pre.get_text(strip=True))
                        if "ip" in json_pre.keys() and "score" in json_pre.keys() and  "risk" in json_pre.keys():
                            json_ret["summary"]["msg"] = "Web方式查询，健康检查成功"
                        else:
                            json_ret["summary"]["statusCode"] = 510
                            json_ret["summary"]["msg"] = "HTML返回数据不符合要求，请查看原始数据"
                    except Exception as e:
                        json_ret["data"]["err_code"] = 500
                        json_ret["data"]["err_msg"] = str(e)
                        json_ret["summary"]["statusCode"] = 512
                        json_ret["summary"]["msg"] = "HTML返回数据不符合要求，请查看原始数据"
                else:
                    json_ret["data"]["err_code"] = 500
                    json_ret["data"]["err_msg"] = "pre = soup.find('pre'),pre为空，请查看原始数据"
                    json_ret["summary"]["statusCode"] = 513
                    json_ret["summary"]["msg"] = "HTML返回数据不符合要求，请查看原始数据"
            else:
                json_ret["data"]["err_code"] = response.status_code
                json_ret["data"]["err_msg"] = response.text
                json_ret["summary"]["statusCode"] = 514
                json_ret["summary"]["msg"] = "Web方式查询，网页请求返回失败，健康检查失败"
        except Exception as e:
            json_ret["data"]["err_code"] = 500
            json_ret["data"]["err_msg"] = str(e)
            json_ret["summary"]["statusCode"] = 514
            json_ret["summary"]["msg"] = "Web方式查询，发现异常，健康检查失败"
    return json_ret

if __name__ == '__main__':
    params = {
        "ip": "104.21.76.129"
    }
    assets = {}
    result = get_ip_fraud_risk_info_from_web(params, assets, None)
    print(json.dumps(result, indent=4))