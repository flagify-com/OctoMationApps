# -*- coding: utf-8 -*-
import json
import urllib
from urllib import request
import bs4


def get_result(ip):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
    url = 'https://scamalytics.com/ip/{0}'.format(ip)
    req = request.Request(url)
    req.add_header('User-Agent', user_agent)
    response = request.urlopen(req)
    content = response.read().decode('utf-8')
    soup = bs4.BeautifulSoup(content, 'html.parser')
    Risk = soup.select('pre')[0].get_text()
    Risk = json.loads(Risk)
    print(Risk)
    score = int(Risk['score'])
    risk = Risk['risk']  # 威胁等级：low: 低,  medium：中， highes: 高
    proxy = soup.select('.risk')
    vpn = True if proxy[0].get_text() == "Yes" else False
    tor = True if proxy[1].get_text() == "Yes" else False
    server = True if proxy[2].get_text() == "Yes" else False
    public = True if proxy[3].get_text() == "Yes" else False
    web = True if proxy[4].get_text() == "Yes" else False
    robot = True if proxy[5].get_text() == "Yes" else False
    return score, risk, vpn, tor, server, public, web, robot


def search_ip(params, assets):
    """查询IP"""
    ip = params["ip"]
    score, risk, vpn, tor, server, public, web, robot = get_result(ip)
    # 返回值
    json_ret = {"code": 200,
                "msg": "",
                "data": {"score": score,
                         "risk": risk,
                         "anonymizing_vpn": vpn,
                         "tor": tor,
                         "server": server,
                         "public_proxy": public,
                         "web_proxy": web,
                         "search_engine_robot": robot}
                }
    return json_ret


if __name__ == '__main__':
    params = {
        "ip": "8.8.8.8"
    }
    assets = {}
    # 查询IP
    print(search_ip(params, assets))
