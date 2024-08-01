#coding: utf-8
import os
import base64


def get_mysql_params_from_env():
    """获取系统AE数据库变量"""
    json_mysql_params = {
        'host': 'mysql.sp.com',
        'port': 3306,
        'database': 'shakespeare_ae',
        'username': 'honeyGuid',    
        'password': '123456',
        'ssl': False
    }
    if 'SHAKESPEARE_AE_DB_HOST' in os.environ:
        json_mysql_params['host'] = os.environ['SHAKESPEARE_AE_DB_HOST']
    if 'SHAKESPEARE_AE_DB_PORT' in os.environ:
        json_mysql_params['port'] = os.environ['SHAKESPEARE_AE_DB_PORT']
    if 'SHAKESPEARE_AE_DB_NAME' in os.environ:
        json_mysql_params['database'] = os.environ['SHAKESPEARE_AE_DB_NAME']
    if 'SHAKESPEARE_AE_DB_USERNAME' in os.environ:
        json_mysql_params['username'] = os.environ['SHAKESPEARE_AE_DB_USERNAME']
    if 'SHAKESPEARE_AE_DB_SSL' in os.environ and os.environ['SHAKESPEARE_AE_DB_SSL'] == 'true':
        json_mysql_params['ssl'] = True
    
    if 'SHAKESPEARE_AE_DB_VP' in os.environ:
        db_vp = os.environ['SHAKESPEARE_AE_DB_VP']
    else:
        db_vp = '123456'

    if 'SHAKESPEARE_AE_DB_PASSWORD' in os.environ:
        db_password = os.environ['SHAKESPEARE_AE_DB_PASSWORD']
    elif 'SHAKESPEARE_AE_DB_VP' in os.environ:
        db_password = '123456'

    if 'SHAKESPEARE_DB_VP_ENC2' in os.environ and os.environ['SHAKESPEARE_DB_VP_ENC2'] == 'false':
        json_mysql_params['password'] = db_vp
        json_mysql_params['root_password'] = db_password
    else:
        raw_db_pwd = base64.b64encode(db_vp.encode()).decode()
        json_mysql_params['password'] =  "?^^{0}1w".format(raw_db_pwd)
        raw_db_password = base64.b64encode(db_password.encode()).decode()
        json_mysql_params['root_password'] = "^${0}".format(raw_db_password)
    return json_mysql_params


def get_mysql_params_for_app_from_env():
    """从环境变量中，为用户自定义的Python APP获取数据库连接参数"""
    json_mysql_params = {
        'host': 'mysql.sp.com',
        'port': 3306,
        'database': 'honeyguide_application',
        'username': 'hg_soar_app',    
        'password': '123456',
        'ssl': False
    }
    if 'SHAKESPEARE_APP_DB_HOST' in os.environ:
        json_mysql_params['host'] = os.environ['SHAKESPEARE_APP_DB_HOST']
    if 'SHAKESPEARE_APP_DB_PORT' in os.environ:
        json_mysql_params['port'] = os.environ['SHAKESPEARE_APP_DB_PORT']
    if 'SHAKESPEARE_APP_DB_NAME' in os.environ:
        json_mysql_params['database'] = os.environ['SHAKESPEARE_APP_DB_NAME']
    if 'SHAKESPEARE_APP_DB_USER' in os.environ:
        json_mysql_params['username'] = os.environ['SHAKESPEARE_APP_DB_USER']
    if 'SHAKESPEARE_APP_DB_SSL' in os.environ and os.environ['SHAKESPEARE_APP_DB_SSL'] == 'true':
        json_mysql_params['ssl'] = True
    
    if 'SHAKESPEARE_APP_DB_VP' in os.environ:
        db_vp = os.environ['SHAKESPEARE_APP_DB_VP']
    else:
        db_vp = '123456'

    if 'SHAKESPEARE_DB_VP_ENC2' in os.environ and os.environ['SHAKESPEARE_DB_VP_ENC2'] == 'false':
        json_mysql_params['password'] = db_vp
    else:
        raw_db_pwd = base64.b64encode(db_vp.encode()).decode()
        json_mysql_params['password'] =  "?^^{0}agh".format(raw_db_pwd)
    return json_mysql_params

def get_mysql_params_from_sdk(hg_client=None):
    """
    根据SDK获取数据库变量
    """
    json_mysql_params = {
        'host': 'mysql.sp.com',
        'port': 3306,
        'database': 'honeyguide_application',
        'username': 'hg_soar_app', 
        'password': '123456',
        'ssl': False
    }
    if hg_client:
        json_mysql_params['host'] = hg_client.dbConfig.getHost(domain="app")
        json_mysql_params['port'] = hg_client.dbConfig.getPort(domain="app")
        # json_mysql_params['database'] = hg_client.dbConfig.getDatabase(domain="app")
        # json_mysql_params['database'] = 'shakespeare_ae'
        json_mysql_params['username'] = hg_client.dbConfig.getUsername(domain="app")
        json_mysql_params['password'] = hg_client.dbConfig.appPassword()
    return json_mysql_params

if __name__ == '__main__':
    print(get_mysql_params_from_env())