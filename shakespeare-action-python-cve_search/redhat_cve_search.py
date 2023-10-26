# -*- coding: utf-8 -*-
import requests


from datetime import datetime
from datetime import timedelta

(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")


def get_cve(params, assets, context_info):
    """获取某个组件的cve信息"""
    
    # 代理
    proxy = None if "proxy" not in assets.keys() or assets["proxy"] == "" else assets["proxy"]

    # 查询日期之前的CVE。[ISO 8601为预期格式] 例 2016-03-01    
    before = None if "before" not in params.keys() or params["before"] == "" else params["before"]

    # 查询日期之后的CVE。[ISO 8601为预期格式] 例 2016-02-01，默认为当前的前一天
    after = str((datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")) if "after" not in params.keys() or params["after"] == "" else params["after"]

    # 用逗号分隔的ID的CVE 例 CVE-2017-8797,CVE-2014-0161
    ids = None if "ids" not in params.keys() or params["ids"] == "" else params["ids"]

    # 严重性 low,moderate,important
    severity = None if "severity" not in params.keys() or params["severity"] == "" else params["severity"]

    # cve影响的包，例nginx
    package = None if "package" not in params.keys() or params["package"] == "" else params["package"]

    # 影响的产品，该参数支持Perl兼容的正则表达式，例 openstack
    product = None if "product" not in params.keys() or params["product"] == "" else params["product"]
    
    # CVSS得分大于或等于该值的CVE，例 7.0
    cvss_score = None if "cvss_score" not in params.keys() or params["cvss_score"] == "" else params["cvss_score"]
    
    # CVSSv3得分大于或等于此值的CVE 例 7.0
    cvss3_score = None if "cvss3_score" not in params.keys() or params["cvss3_score"] == "" else params["cvss3_score"]
    
    # 分页，页数
    page = 1 if "page" not in params.keys() or params["page"] == "" else params["page"]
    # 分页大小
    per_page = 10 if "per_page" not in params.keys() or params["per_page"] == "" else params["per_page"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"records":[{"CVE": "", "severity": "", "public_date": "", "advisories": "", "bugzilla": "", "bugzilla_description": "", "cvss_score": "", "cvss_scoring_vector": "", "CWE": "", "affected_packages": "", "resource_url": "", "cvss3_scoring_vector": "", "cvss3_score": ""}]}}

    params = {"before":before,"after":after,"ids":ids,"severity":severity,"package":package,"product":product,"cvss_score":cvss_score,"cvss3_score":cvss3_score,"page":page,"per_page":per_page}

    proxies = {"http:":proxy,"https":proxy}
    
    url = "https://access.redhat.com/labs/securitydataapi/cve.json"
    
    try:
        r = requests.get(url, params=params, timeout=20, proxies=proxies).json()
        json_ret["data"]["records"] = r
    except Exception as e:
        json_ret["code"] = 500
        json_ret["msg"] = str(e)

    return json_ret


def get_cve_details(params, assets, context_info):
    """检索完整的CVE详细信息"""

    # 代理
    proxy = None if "proxy" not in assets.keys() or assets["proxy"] == "" else assets["proxy"]

    # cve id 例 CVE-2016-3706
    cve_id = params["id"]

    # 返回值
    json_ret = {"code": 200, "msg": "","data": {"threat_severity": "", "public_date": "", "bugzilla": "", "cvss3": "", "cwe": "", "details": "", "affected_release": "", "package_state": "", "upstream_fix": "", "references": "", "name": "", "csaw": ""}}

    url = f"https://access.redhat.com/hydra/rest/securitydata/cve/{cve_id.upper()}.json"
    proxies = {"http:":proxy,"https":proxy}

    try:
        r = requests.get(url, timeout=20, proxies=proxies).json()
        json_ret["data"] = r
    except Exception as e:
        json_ret["code"] = 500
        json_ret["msg"] = str(e)

    return json_ret


if __name__ == "__main__":
    params = {"id":"CVE-2016-3706"} 
    assets = {} 
    context_info = {}
    r = get_cve_details(params, assets, context_info)
    print(r)
    
    