# -*- coding: utf-8 -*-
import requests
from urllib.parse import urlencode, urljoin
from datetime import datetime, timezone, timedelta

def health_check(params, assets, context_info):
    """健康检查"""
    proxy = assets.get("proxy", None)
    json_ret = {"code": 200, "msg": "", "data": {"cve_id": ""}, "summary": {"statusCode": 200, "msg": "ok"}}
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-44228"
    proxies = {"http:": proxy, "https": proxy}
    try:
        r = requests.get(url, timeout=20, proxies=proxies).json()
        json_ret["data"]["cve_id"] = r["vulnerabilities"][0]["cve"]["id"]
    except requests.RequestException as e:
        json_ret["code"] = 500
        json_ret["msg"] = str(e)
        json_ret["summary"]["statusCode"] = 400
        json_ret["summary"]["msg"] = str(e)
    return json_ret

def cves(params, assets, context_info):
    """获取cve数据"""
    json_ret = {"code": 200, "msg": "", "data": {"records":[]}}
    current_time_with_timezone = datetime.now(timezone(timedelta(hours=8)))
    proxy = assets.get("proxy", None)
    keyword_search = params.get("keywordSearch", "chrome")
    
    # pubStartDate，默认为前一天
    pub_start_date = params.get("pubStartDate")
    if pub_start_date:
        try:
            pub_start_date = datetime.strptime(pub_start_date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(timedelta(hours=8)))
        except ValueError as e:
            return handle_date_error(json_ret, e)
    else:
        pub_start_date = current_time_with_timezone - timedelta(days=1)

    # pubEndDate默认为今天
    pub_end_date = params.get("pubEndDate")
    if pub_end_date:
        try:
            pub_end_date = datetime.strptime(pub_end_date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(timedelta(hours=8)))
        except ValueError as e:
            return handle_date_error(json_ret, e)
    else:
        pub_end_date = current_time_with_timezone
        
    # 检查pubStartDate和pubEndDate相差是否超过120天
    if (pub_end_date - pub_start_date).days > 120:
        json_ret["code"] = 400
        json_ret["msg"] = "pubStartDate and pubEndDate 间隔不能超过120天"
        return json_ret

    # cvssV3Severity
    cvssV3Severity = params.get("cvssV3Severity", "")
    
    results_per_page = params.get("resultsPerPage", 10)
    start_index = params.get("startIndex", 0)

    params = {
        "keywordSearch": keyword_search,
        "pubStartDate": pub_start_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + pub_start_date.strftime("%z")[:3] + ":" + pub_start_date.strftime("%z")[3:],
        "pubEndDate": pub_end_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + pub_end_date.strftime("%z")[:3] + ":" + pub_end_date.strftime("%z")[3:],
        "resultsPerPage": results_per_page,
        "startIndex": start_index
    }
    
    if cvssV3Severity:
        params["cvssV3Severity"] = cvssV3Severity
    
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/"
    url = urljoin(base_url, "?" + urlencode(params, safe=':/'))
    
    proxies = {"http:": proxy, "https": proxy}
    try:
        r = requests.get(url, timeout=20, proxies=proxies).json()
        cve_data = r["vulnerabilities"]
        if len(cve_data) > 0:
            for row in cve_data:
                descriptions = row["cve"]["descriptions"][0]['value'] if row["cve"]["descriptions"] else ""
                references = row["cve"]["references"][0]["url"] if row["cve"]["references"] else ""

                row_data = {"cve_id":row["cve"]["id"],"descriptions":descriptions,"published":row["cve"]["published"],"references":references}
                json_ret["data"]["records"].append(row_data)
        
        json_ret["data"]["resultsPerPage"] = r["resultsPerPage"]
        json_ret["data"]["startIndex"] = r["startIndex"]
        json_ret["data"]["totalResults"] = r["totalResults"]
    except requests.RequestException as e:
        json_ret["code"] = 500
        json_ret["msg"] = str(e)
    return json_ret

def handle_date_error(json_ret, e):
    json_ret["code"] = 400
    json_ret["msg"] = str(e)
    return json_ret
