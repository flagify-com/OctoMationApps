# -*- coding: utf-8 -*-
import requests
import json

def create_issue(params, assets, context_info):
    """创建一个GitHub Issue"""

    # 所有者，即用户或者组织名（https://github.com/octo-org/octo-repo， owner：octo-org）
    owner = assets["owner"]
    # 代码仓库名称（https://github.com/octo-org/octo-repo， 仓库名：octo-repo）
    repository = assets["repository"]
    # Personal Access Token
    pat_token = assets["pat_token"]
    # GitHub Issue的标题
    issue_title = params["issue_title"]
    # GitHub Issue的内容
    issue_body = params["issue_body"]
    # GitHub Issue的标签
    issue_labels = [] if "issue_labels" not in params.keys() or params["issue_labels"] == "" else params["issue_labels"]
    issue_assignees = [] if "issue_assignees" not in params.keys() or params["issue_assignees"] == "" else params["issue_assignees"]
    Proxies = None
    if 'http_proxy' in assets.keys() and assets['http_proxy'] != '':
        http_proxy = assets['http_proxy']
        Proxies = {
            "http": http_proxy,
            "https": http_proxy
        }

    # 返回值
    json_ret = {"code": -1, "msg": "","data": {"success": False, "issue_number":  None, "issue_api_url": "", "issue_html_url": ""}}

    '''添加函数实现
    
    '''

    url = f"https://api.github.com/repos/{owner}/{repository}/issues"
    headers = {
        "Authorization": f"Bearer {pat_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    data = {
        "title": issue_title,
        "body": issue_body
    }
    if issue_labels != []:
        data ['labels'] = [issue_labels]
    if issue_assignees != []:
        data ['assignees'] = [issue_assignees]
    # print(json.dumps(data))
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), proxies=Proxies, timeout=60)
        if response.status_code == 201:
            json_res = response.json()
            json_ret['data']['issue_number'] = json_res['number']
            json_ret['data']['issue_api_url'] = json_res['url']
            json_ret['data']['issue_html_url'] = json_res['html_url']
            json_ret['data']['success'] = True
            json_ret['msg'] = "创建成功"
            json_ret['code'] = 200
            print('Successfully created Issue "{0}", {1}'.format(issue_title, json_ret['data']['issue_html_url']))
        else:
            json_ret['code'] = response.status_code
            json_ret['msg'] = response.text
            print('Could not create Issue "{0}"'.format(issue_body))
            print('Response:', response.content)
    except Exception as e:
        json_ret['msg'] = str(e)
        print(e)

    return json_ret

def update_issue(params, assets, context_info):
    """更新一个GitHub Issue"""

    # 所有者，即用户或者组织名（https://github.com/octo-org/octo-repo， owner：octo-org）
    owner = assets["owner"]
    # 代码仓库名称（https://github.com/octo-org/octo-repo， 仓库名：octo-repo）
    repository = assets["repository"]
    # Personal Access Token
    pat_token = assets["pat_token"]

    issue_number = 0 if "issue_number" not in params.keys() or params["issue_number"] == "" else params["issue_number"]
    issue_title = "" if "issue_title" not in params.keys() or params["issue_title"] == "" else params["issue_title"]
    issue_body = "" if "issue_body" not in params.keys() or params["issue_body"] == "" else params["issue_body"]
    issue_labels = [] if "issue_labels" not in params.keys() or params["issue_labels"] == "" else params["issue_labels"]
    issue_state = "" if "issue_state" not in params.keys() or params["issue_state"] == "" else params["issue_state"]
    issue_state_reason = None if "issue_state_reason" not in params.keys() or params["issue_state_reason"] == "" else params["issue_state_reason"]
    issue_assignees = [] if "issue_assignees" not in params.keys() or params["issue_assignees"] == "" else params["issue_assignees"]
    
    Proxies = None
    if 'http_proxy' in assets.keys() and assets['http_proxy'] != '':
        http_proxy = assets['http_proxy']
        Proxies = {
            "http": http_proxy,
            "https": http_proxy
        }

    # 返回值
    json_ret = {"code": -1, "msg": "","data": {"success": False}}

    '''添加函数实现
    
    '''

    url = f"https://api.github.com/repos/{owner}/{repository}/issues/{issue_number}"
    headers = {
        "Authorization": f"Bearer {pat_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    data = {}
    if issue_title != "":
        data ['title'] = issue_title
    if issue_body != "":
        data ['body'] = issue_body
    if issue_assignees != []:
        data ['assignees'] = [issue_assignees]
    if issue_state != "":
        data ['state'] = issue_state
    if issue_state_reason != "":
        data ['state_reason'] = issue_state_reason
    if issue_labels != []:
        data ['lables'] = [issue_labels]
    print(json.dumps(data))
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), proxies=Proxies, timeout=60)
        if response.status_code == 200:
            json_res = response.json()
            if 'number' in json_res.keys() and json_res['number'] == issue_number:
                json_ret['data']['success'] = True
                json_ret['msg'] = "更新成功"
                json_ret['data']['issue_api_url'] = json_res['url']
                json_ret['data']['issue_html_url'] = json_res['html_url']
                json_ret['code'] = 200
                print('Successfully updated Issue "{0}", {1}'.format(issue_number, json_ret['data']['issue_html_url']))
        else:
            json_ret['code'] = response.status_code
            json_ret['msg'] = response.text
            print('Could not update Issue {0}'.format(issue_number))
            print('Response:', response.content)
    except Exception as e:
        json_ret['msg'] = str(e)
        print(e)

    return json_ret

def test(params, assets, context_info):
    """ 测试"""

    # 所有者，即用户或者组织名（https://github.com/octo-org/octo-repo， owner：octo-org）
    owner = assets["owner"]
    # 代码仓库名称（https://github.com/octo-org/octo-repo， 仓库名：octo-repo）
    repository = assets["repository"]
    # Personal Access Token
    pat_token = assets["pat_token"]

    # 返回值
    json_ret = {"code": -1, "msg": "测试失败","data": {"success": False}}

    '''添加函数实现
    
    '''
    Proxies = None
    if 'http_proxy' in assets.keys() and assets['http_proxy'] != '':
        http_proxy = assets['http_proxy']
        Proxies = {
            "http": http_proxy,
            "https": http_proxy
        }

    url = f"https://api.github.com/repos/{owner}/{repository}/issues"
    headers = {
        "Authorization": f"Bearer {pat_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    try:
        response = requests.get(url, headers=headers, proxies=Proxies, timeout=60)
        json_ret['code'] = response.status_code
        if response.status_code == 200:
            json_ret['msg'] = "测试成功"
    except Exception as e:
        json_ret['msg'] = str(e)
        print(e)

    return json_ret
