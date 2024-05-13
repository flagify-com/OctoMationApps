#coding:utf-8
import requests
import json
import os   
import time
from core_wework_access_token import get_access_token

class WeWorkGroupAdmin:
    def __init__(self, app_id, corp_id, corp_secret, apiserver_base_uri):
        self.app_id = app_id
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.apiserver_base_uri = apiserver_base_uri
    
    def get_access_token(self):
        return get_access_token(self.app_id, self.corp_id, self.corp_secret)
    
    def create_group(self, group_userlist=[], group_name=None, group_owner=None, group_chatid=None ):
        """
        创建群聊
        :param group_userlist: 群成员列表，成员ID列表
        :param group_name: 群名
        :param group_owner: 群主ID    
        :param group_chatid: 群聊id，指定后不能与群名同时为空
        :return: errcode, errmsg, 群聊id
        """

        json_ret = {
            "errcode": -1,
            "errmsg": "Unknown Error",
            "chatid": None
        }
        json_access_token = self.get_access_token()
        access_token = json_access_token['access_token']
        if access_token is None:
            json_ret['errmsg'] = json_access_token['errmsg']
            json_ret['errcode'] = json_access_token['errcode']
            return json_ret
        url = f'{self.apiserver_base_uri}/appchat/create?access_token=%s' % access_token
        data = {
            "chatid": group_chatid, # 群聊id，指定后不能与群名同时为空
            "name": group_name, # 群名，指定后不能与群聊id同时为空
            "owner": group_owner, # 群主id
            "userlist": group_userlist # 群成员列表
        }
        try:
            response = requests.post(url, data=json.dumps(data))
            json_ret['errcode'] = response.status_code

            if response.status_code == 200:
                json_response = json.loads(response.text)
                json_ret['errcode'] = json_response['errcode']
                json_ret['errmsg'] = json_response['errmsg']
                if json_response['errcode'] == 0:
                    json_ret['chatid'] = json_response['chatid']
            else:
                json_ret['errmsg'] = 'create group failed, HTTP status_code: %s' % response.status_code
        except Exception as e:
            json_ret['errmsg'] = str(e)
        return json_ret
    
    def update_group(self, group_chatid, group_name=None, group_owner=None, add_userlist=[], del_userlist=[]):
        """
        更新群聊
        :param group_chatid: 群聊id
        :param add_userlist: 新增成员列表
        :param del_userlist: 踢出成员列表
        :param group_name: 群名
        :param group_owner: 群主ID
        :return: errcode, errmsg
        """

        json_ret = {
            "errcode": -1,
            "errmsg": "Unknown Error"
        }
        json_access_token = self.get_access_token()
        access_token = json_access_token['access_token']
        if access_token is None:
            json_ret['errmsg'] = json_access_token['errmsg']
            json_ret['errcode'] = json_access_token['errcode']
            return json_ret
        url = f'{self.apiserver_base_uri}/appchat/update?access_token=%s' % access_token
        data = {
            "chatid": group_chatid, # 群聊id
            "name": group_name, # 群名
            "owner": group_owner, # 群主id
            "add_user_list": add_userlist, # 新增成员列表
            "del_user_list": del_userlist # 踢出成员列表
        }
        try:
            response = requests.post(url, data=json.dumps(data))
            json_ret['errcode'] = response.status_code

            if response.status_code == 200:
                json_response = json.loads(response.text)
                json_ret['errcode'] = json_response['errcode']
                json_ret['errmsg'] = json_response['errmsg']
            else:
                json_ret['errmsg'] = 'update group failed, HTTP status_code: %s' % response.status_code
        except Exception as e:
            json_ret['errmsg'] = str(e)
        return json_ret

    def send_group_text_message(self, group_chatid, content, safe=0):

        """
        发送群聊文本消息
        :param group_chatid: 群聊id
        :param content: 消息内容
        :param safe: 表示是否是保密消息，0表示否，1表示是，默认0
        :return: errcode, errmsg, 消息id
        """

        json_ret = {
            "errcode": -1,
            "errmsg": "Unknown Error"
        }
        json_access_token = self.get_access_token()
        access_token = json_access_token['access_token']
        if access_token is None:
            json_ret['errmsg'] = json_access_token['errmsg']
            json_ret['errcode'] = json_access_token['errcode']
            return json_ret
        url = f'{self.apiserver_base_uri}/appchat/send?access_token=%s' % access_token
        data = {
            "chatid": group_chatid, # 群聊id
            "msgtype": "text", # 消息类型，此处为文本消息
            "text": {
                "content": content # 消息内容
            },
            "safe": safe # 表示是否是保密消息，0表示否，1表示是，默认0
        }
        try:
            response = requests.post(url, data=json.dumps(data))
            json_ret['errcode'] = response.status_code
            if response.status_code == 200: # 请求成功
                json_response = json.loads(response.text)
                json_ret['errcode'] = json_response['errcode']
                json_ret['errmsg'] = json_response['errmsg']
            else:
                json_ret['errmsg'] ='send group text message failed, HTTP status_code: %s' % response.status_code
        except Exception as e:
            json_ret['errmsg'] = str(e)
        return json_ret

    def get_group_chat_info(self, group_chatid):
        """
        获取群聊信息    
        :param group_chatid: 群聊id
        :return: errcode, errmsg, 群聊信息
        """

        json_ret = {
            "errcode": -1,
            "errmsg": "Unknown Error"
        }
        json_access_token = self.get_access_token()
        access_token = json_access_token['access_token']
        if access_token is None:
            json_ret['errmsg'] = json_access_token['errmsg']
            json_ret['errcode'] = json_access_token['errcode']
            return json_ret
        url = f'{self.apiserver_base_uri}/appchat/get?access_token=%s&chatid=%s' % (access_token, group_chatid)
        try:
            response = requests.get(url)
            json_ret['errcode'] = response.status_code
            if response.status_code == 200: # 请求成功
                json_response = json.loads(response.text)
                json_ret['errcode'] = json_response['errcode']
                json_ret['errmsg'] = json_response['errmsg']
                json_ret['chat_info'] = json_response['chat_info']
            else:
                json_ret['errmsg'] = 'get group chat info failed, HTTP status_code: %s' % response.status_code
        except Exception as e:
            json_ret['errmsg'] = str(e)
        return json_ret
        
if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    load_dotenv()

    appid = os.getenv('APPID')
    corpid = os.getenv('CORPID')
    corpsecret = os.getenv('CORPSECRET')
    wework_group_admin = WeWorkGroupAdmin(appid, corpid, corpsecret)

    # 创建群聊
    # group_userlist = ['Fukui', 'GouGou']
    # group_owner = 'Fukui'
    # group = wework_group_admin.create_group(group_userlist=group_userlist, group_name='测试群聊', group_owner=group_owner)
    # print(group)

    chatid = 'wrMviBDgAAuHcpi_9uZBLxA7DByli6sw'
    group = wework_group_admin.get_group_chat_info(group_chatid=chatid)
    print(group)

    # 更新群聊    
    # add_userlist = ['YiChangYouXiYiChangMeng','PPP']
    # del_userlist = ['GouGou']
    # group = wework_group_admin.update_group(group_chatid=chatid, add_userlist=add_userlist, del_userlist=del_userlist)
    # print(group)

    # # 发送群聊文本消息
    # content = 'Hello, WeWork!'
    # message = wework_group_admin.send_group_text_message(group_chatid=chatid, content=content)
    # print(message)