from wework_group_admin import create_appchat_group, update_appchat_group,  get_appchat_group, send_appchat_group_text
# # pip install python-dotenv
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()
corpid = os.getenv('CORPID')
corpsecret = os.getenv('CORPSECRET')

def test_create_appchat_group():
    params = {
        'group_name': 'test_group',
        'group_owner': 'Fukui',
        'group_userids': 'Fukui, YiChangYouXiYiChangMeng'
    }
    assets = {
        'apiserver_base_uri': 'https://qyapi.weixin.qq.com/cgi-bin',
        'corpid': corpid,
        'corpsecret': corpsecret
    }
    context_info = None

    json_ret = create_appchat_group(params, assets, context_info)
    print(json_ret)

def test_update_appchat_group():
    params = {
        'group_chatid': 'wrMviBDgAAdfxaVhxQ8MbnFAbzGc19eA',
        'group_add_userids': 'GouGou',
        'group_del_userids': 'YiChangYouXiYiChangMeng'
    }
    assets = {
        'apiserver_base_uri': 'https://qyapi.weixin.qq.com/cgi-bin',
        'corpid': corpid,
        'corpsecret': corpsecret
    }
    context_info = None

    json_ret = update_appchat_group(params, assets, context_info)
    print(json_ret)

def test_get_appchat_group():
    params = {
        'group_chatid': 'wrMviBDgAAdfxaVhxQ8MbnFAbzGc19eA'
    }
    assets = {
        'apiserver_base_uri': 'https://qyapi.weixin.qq.com/cgi-bin',
        'corpid': corpid,
        'corpsecret': corpsecret
    }
    context_info = None
    json_ret = get_appchat_group(params, assets, context_info)
    print(json_ret)

def test_send_appchat_group_text():
    params = {
        'group_chatid': 'wrMviBDgAAdfxaVhxQ8MbnFAbzGc19eA',
        'text': 'Hello, WeWork Group Admin!'
    }
    assets = {
        'apiserver_base_uri': 'https://qyapi.weixin.qq.com/cgi-bin',
        'corpid': corpid,
        'corpsecret': corpsecret
    }
    context_info = None
    json_ret = send_appchat_group_text(params, assets,context_info)
    print(json_ret)

if __name__ == '__main__':
    # test_create_appchat_group()
    # test_update_appchat_group()
    test_get_appchat_group()
    # test_send_appchat_group_text()
