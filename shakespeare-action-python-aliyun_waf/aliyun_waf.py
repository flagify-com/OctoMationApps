# -*- coding: utf-8 -*-
import json
import logging
import random
import re
import time

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkwaf_openapi.request.v20190910.CreateProtectionModuleRuleRequest import CreateProtectionModuleRuleRequest
from aliyunsdkwaf_openapi.request.v20190910.DescribeDomainListRequest import DescribeDomainListRequest
from aliyunsdkwaf_openapi.request.v20190910.DescribeInstanceInfosRequest import DescribeInstanceInfosRequest
from aliyunsdkwaf_openapi.request.v20190910.DescribeProtectionModuleRulesRequest import \
    DescribeProtectionModuleRulesRequest
from aliyunsdkwaf_openapi.request.v20190910.DescribeProtectionModuleStatusRequest import \
    DescribeProtectionModuleStatusRequest
from aliyunsdkwaf_openapi.request.v20190910.ModifyProtectionModuleModeRequest import ModifyProtectionModuleModeRequest
from aliyunsdkwaf_openapi.request.v20190910.ModifyProtectionModuleStatusRequest import \
    ModifyProtectionModuleStatusRequest

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d]'
                           ' - %(levelname)s : %(message)s        --(%(funcName)s)')
logger = logging.getLogger(__name__)


class AliyunWAF:
    def __init__(self, service_address, domain_id, accesskey_id, accesskey_secret):
        self.service_address = service_address
        self.domain_id = domain_id
        self.accesskey_id = accesskey_id
        self.accesskey_secret = accesskey_secret
        self.generate_client()  # 生成全局通用请求对象

        # 通用
        self.code = 200  # 全局状态码
        self.error_msg = ""  # 错误输出信息
        self.source_data = ""
        self.info_list = list()  # 标准输出（一个字典）
        self.count_num = 1

    def cut_ip(self, host):
        """进行IP/MAC判断与切割，返回IP列表，如['192.168.200.185', '192.168.200.186']"""
        ips = list()
        hosts = host.split(",")
        ip_re = re.compile(
            "^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])."
            "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)."
            "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)."
            "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$")
        mac_re = re.compile("^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$")
        for ip in hosts:
            if re.match(ip_re, ip):
                ips.append(ip)
            elif re.match(mac_re, ip):
                ips.append(ip)
        return ips

    def info_trans(self, old_dict):
        """信息转换，例如{'Status': 0, 'EndDate': 1512921600}  -> {'Status': '已到期', 'EndDate': '2017-12-11'}"""
        logger.debug(old_dict)
        new_values = {}
        new_values["Status"] = {0: "已到期", 1: "正常"}
        new_values["PayType"] = {0: "未购买或未开通WAF", 1: "包年包月", 2: "按量付费"}

        try:
            old_dict['PayType'] = new_values['PayType'][old_dict['PayType']]
            old_dict['Status'] = new_values['Status'][old_dict['Status']]
            old_dict["EndDate"] = time.strftime('%Y-%m-%d', time.localtime(old_dict["EndDate"]))
        except Exception as e:
            print(e)
        return old_dict

    def replace_keys(self, old_dict):
        """替换字典key，例如：{"a":1, "b": 2, "c":3} -> {'A': 1, 'B': 2, 'C': 3}"""
        new_dict = {}
        new_keys = {"Status": "状态", "EndDate": "到期时间", "InstanceId": "实例ID", "error": "错误信息",
                    "PayType": "实例类型"}
        for old_key in old_dict:
            try:
                new_dict[new_keys[old_key]] = old_dict[old_key]
            except Exception as e:
                pass
        return new_dict

    def json_clean(self, data):
        """
        用于格式化格式，返回列表    供前端显示用 将jsons = {"1": "one", 2": "two","3": "three" } ->
         [{'name': '1', 'value': 'one'}, {'name': '2', 'value': 'two'}, {'name': '3', 'value': 'three'}]
        """
        for info in data.keys():
            info_temporary = {}
            info_temporary["name"] = info
            info_temporary["value"] = data[info]
            self.info_list.append(info_temporary)

    def generate_client(self):
        """生成一个会话对象，并初始化信息"""
        self.client = AcsClient(f'{self.accesskey_id}', f'{self.accesskey_secret}', self.domain_id)

    def get_instanceid(self):
        """获取实例信息"""
        try:
            request = DescribeInstanceInfosRequest()
            request.set_accept_format('json')
            response = self.client.do_action_with_exception(request)
            logger.info(str(response))
            self.source_data += str(response)
            response_json = json.loads(response)
            target_list = response_json["InstanceInfos"]

        except Exception as e:
            self.code = 500
            self.error_msg += str(e) + ";"
            target_list = [{'Status': 0, 'SubscriptionType': 'null', 'InstanceId': f'{str(e)}', 'InDebt': 0, 'Region': 'null', 'PayType': 0, 'EndDate': 0}]
        logger.debug(target_list)
        return target_list

    def health_check_main(self):
        instance_list = self.get_instanceid()
        if instance_list:
            for instance in instance_list:
                new_dict = self.info_trans(instance)
                new_dict = self.replace_keys(new_dict)
                self.info_list.append(new_dict)
        return self.code, self.error_msg, self.info_list, self.source_data

    def get_domain_assets(self, instance_id):
        try:
            request = DescribeDomainListRequest()
            request.set_accept_format('json')
            request.set_InstanceId(instance_id)
            response = self.client.do_action_with_exception(request)
            self.source_data = str(response)
            logger.info(response)
            response_json = json.loads(response)
            # # 假设成功
            # response_json = {
            #   "DomainNames": [
            #     "1.example.com",
            #     "2.example.com",
            #     "3.example.com"
            #   ],
            #   "RequestId": "D7861F61-5B61-46CE-A47C-6B19160D5EB0"
            # }

            target_msg = response_json["DomainNames"]  # 提取需要的元素
        except Exception as e:
            self.code = 500
            self.error_msg += str(e) + ";"
            target_msg = {"error": str(e)}
        logger.debug(target_msg)
        return target_msg

    def get_domain_assets_main(self, instance_id):
        """获取域名资产信息"""
        domain_list = self.get_domain_assets(instance_id)
        # 清洗一下返回的列表
        domain_dict = {}
        for domain in domain_list:
            domain_dict[self.count_num] = domain
            self.count_num += 1
        self.json_clean(domain_dict)
        if not self.info_list: self.info_list.append({"name": "空数值", "value": "请登录waf确认输入的实例ID是否有对应的域名"})
        return self.code, self.error_msg, self.info_list, self.source_data

    def change_pro_mode(self):
        try:
            request = ModifyProtectionModuleModeRequest()
            request.set_accept_format('json')
            response = self.client.do_action_with_exception(request)
            self.source_data = str(response)
            logger.info(response)
            response_json = json.loads(response)
            # # 假设成功
            # response_json = {
            #   "DomainNames": [
            #     "1.example.com",
            #     "2.example.com",
            #     "3.example.com"
            #   ],
            #   "RequestId": "D7861F61-5B61-46CE-A47C-6B19160D5EB0"
            # }

            target_msg = response_json["DomainNames"]  # 提取需要的元素
        except Exception as e:
            self.code = 500
            self.error_msg += str(e) + ";"
            target_msg = {"error": str(e)}
        logger.debug(target_msg)
        return target_msg

    def modify_protection_module_status(self, domain, module_status, instance_id, defense_type):
        try:
            request = ModifyProtectionModuleStatusRequest()
            request.set_accept_format('json')

            request.set_Domain(f"{domain}")
            request.set_InstanceId(f"{instance_id}")
            request.set_DefenseType(f"{defense_type}")
            request.set_ModuleStatus(module_status)
            response = self.client.do_action_with_exception(request)
            self.source_data = str(response)
            logger.info(response)
            target_msg = json.loads(response)

            self.info_list.append({"name": f"{defense_type}", "value": "操作成功"})
        except Exception as e:
            self.code = 500
            self.error_msg += str(e) + ";"
            target_msg = {"error": str(e)}
            self.info_list.append({"name": f"{defense_type}", "value": str(e)})
        logger.debug(target_msg)
        return target_msg

    def modify_protection_module_status_main(self, domain, module_status, instance_id, defense_type):
        """打开或关闭指定WAF防护功能"""
        self.modify_protection_module_status(domain, module_status, instance_id, defense_type)
        return self.code, self.error_msg, self.info_list, self.source_data

    def describe_protection_module_rules(self, domain, instance_id, defense_type="ac_blacklist"):
        """需要查询黑名单规则信息直接调我即可"""
        try:
            request = DescribeProtectionModuleRulesRequest()
            request.set_accept_format('json')

            request.set_InstanceId(f"{instance_id}")
            request.set_DefenseType(f"{defense_type}")
            request.set_Domain(f"{domain}")

            response = self.client.do_action_with_exception(request)
            self.source_data = str(response)
            logger.info(response)
            target_msg = json.loads(response)
            if "Message" in target_msg.keys():
                rule_id = "error"
                target_msg = target_msg["Message"]
            else:
                rule_id = target_msg["Rules"][0]["RuleId"]
                target_msg = target_msg["Rules"][0]["Content"]["remoteAddr"]

        except Exception as e:
            self.code = 500
            self.error_msg += str(e) + ";"
            target_msg = []
            rule_id = "error"
        logger.debug(target_msg)
        return target_msg, rule_id

    def describe_protection_module_rules_main(self, domain, instance_id):
        """获取黑名单组"""
        info_list, rule_id = self.describe_protection_module_rules(domain, instance_id)
        logger.info(info_list)
        self.info_list.append({"name": "现存数量", "value": str(len(info_list))})
        self.info_list.append({"name": "IP组", "value": str(info_list)})
        self.info_list.append({"name": "规则ID", "value": rule_id})
        return self.code, self.error_msg, self.info_list, self.source_data

    def sent_header(self, req_type):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain(f'{self.service_address}')
        request.set_method(f'{req_type}')
        request.set_protocol_type('https')  # https | http
        request.set_version('2019-09-10')
        return request

    def add_blackip(self, domain, instance_id, ip_list, rule_id, defense_type="ac_blacklist",
                    lockversion=random.randint(1, 999)):
        try:
            request = self.sent_header(req_type="POST")
            request.set_action_name('ModifyProtectionModuleRule')

            request.add_query_param('InstanceId', f"{instance_id}")
            request.add_query_param('Domain', f"{domain}")
            request.add_query_param('DefenseType', f"{defense_type}")
            request.add_query_param('Rule', f"{{'remoteAddr':{ip_list}}}")
            request.add_query_param('RuleId', f"{rule_id}")
            request.add_query_param('LockVersion', f"{lockversion}")

            response = self.client.do_action_with_exception(request)
            self.source_data = str(response)
            logger.info(response)
            target_msg = json.loads(response)
            if "Message" in target_msg.keys():
                target_msg = target_msg["Message"]
            else:
                target_msg = "黑名单现有IP"
        except Exception as e:
            self.code = 500
            self.error_msg += str(e) + ";"
            target_msg = str(e)
        self.info_list.append({"name": f"{target_msg}", "value": f"{ip_list}"})
        logger.debug(target_msg)

    def add_blackip_main(self, domain, instance_id, blackip, group_max_num=200):
        # blackip重装未list
        ip_list = self.cut_ip(blackip)
        # 获取源IP组、数量、规则ID
        black_iplist, rule_id = self.describe_protection_module_rules(domain, instance_id)
        # 组装新组，当组数量大于200时，报错并不再发起请求
        new_black_list = list(set(ip_list + black_iplist))
        if len(new_black_list) > group_max_num:
            self.info_list.append({"name": f"操作失败：新IP({len(ip_list)})+源IP({len(black_iplist)})数量超过阈值{group_max_num}",
                                   "value": f"请删减新增IP数量或使用移除功能删除部分功能"})
        else:
            # 发起请求，如果Message字段没在key里面则视为请求成功
            self.add_blackip(domain=domain, instance_id=instance_id, ip_list=new_black_list, rule_id=rule_id)
        return self.code, self.error_msg, self.info_list, self.source_data

    def remove_blackip_main(self, domain, instance_id, blackip):
        """IP移出黑名单"""
        # blackip重装未list
        ip_list = self.cut_ip(blackip)
        # 获取源IP组、数量、规则ID
        black_iplist, rule_id = self.describe_protection_module_rules(domain, instance_id)
        # 匹配、移除
        for ip in ip_list:
            try:
                black_iplist.remove(ip)
                self.info_list.append({"name": f"{ip}", "value": "操作成功"})
            except Exception as e:
                self.info_list.append({"name": f"{ip}", "value": "操作失败，IP不存在"})
                self.error_msg = 500
                continue
        self.add_blackip(domain=domain, instance_id=instance_id, ip_list=black_iplist, rule_id=rule_id)
        return self.code, self.error_msg, self.info_list, self.source_data

    def add_whilelist(self, domain, instance_id, whileip, if_belong,
                      defense_type="whitelist", name=int(time.time())):
        try:
            request = CreateProtectionModuleRuleRequest()
            request.set_accept_format('json')

            request.set_DefenseType(f"{defense_type}")
            request.set_Domain(f"{domain}")
            request.set_Rule("{{'name':'soar_{0}','tags':['blacklist'],'conditions':[{{'opCode':{1},'key':'IP',"
                             "'values':'{2}'}}]}}".format(name, if_belong, whileip))
            request.set_InstanceId(f"{instance_id}")

            response = self.client.do_action_with_exception(request)
            self.source_data = str(response)
            logger.info(response)
            target_msg = json.loads(response)
            if "Message" in target_msg.keys():
                target_msg = target_msg["Message"]
            else:
                target_msg = f"操作成功 - soar_{name}"
        except Exception as e:
            self.code = 500
            self.error_msg += str(e) + ";"
            target_msg = str(e)
        self.info_list.append({"name": f"{target_msg}", "value": f"{whileip}"})
        logger.debug(target_msg)

    def add_whilelist_main(self, domain, instance_id, whileip, if_belong):
        """添加黑名单"""
        print(domain, instance_id, whileip)
        self.add_whilelist(domain, instance_id, whileip, if_belong)
        return self.code, self.error_msg, self.info_list, self.source_data

    def get_pro_module_status(self, domain, instance_id, module_name):
        try:
            request = DescribeProtectionModuleStatusRequest()
            request.set_accept_format('json')

            request.set_Domain(f"{domain}")

            request.set_DefenseType(f"{module_name}")
            request.set_InstanceId(f"{instance_id}")

            response = self.client.do_action_with_exception(request)
            self.source_data = str(response)
            logger.info(response)
            target_msg = json.loads(response)
            status = {0: "关闭", 1: '开启'}
            if "Message" in target_msg.keys():
                target_msg = target_msg["Message"]
            else:
                target_msg = status[target_msg['ModuleStatus']]
        except Exception as e:
            self.code = 500
            self.error_msg += str(e) + ";"
            target_msg = str(e)
        logger.debug(target_msg)
        return target_msg

    def get_pro_module_status_main(self, domain, instance_id):
        """查询WAF各防护功能的状态"""
        modules = {
            'waf': '规则防护引擎',
            'dld': '深度学习引擎',
            'tamperproof': '网站防篡改',
            'dlp': '防敏感信息泄漏',
            'normalized': '主动防御',
            'bot_crawler': '合法爬虫',
            'bot_intelligence': '爬虫威胁情报',
            'antifraud': '数据风控',
            'bot_algorithm': '智能算法',
            'bot_wxbb': 'App防护',
            'bot_wxbb_pkg': 'App防护中的版本防护',
            'ac_cc': 'CC安全防护',
            'ac_blacklist': 'IP黑名单',
            'ac_highfreq': '扫描防护中的高频Web攻击封禁',
            'ac_dirscan': '扫描防护中的目录扫描防护',
            'ac_scantools': '扫描防护中的扫描工具封禁',
            'ac_collaborative': '扫描防护中的协同防御',
            'ac_custom': '自定义防护策略'
        }

        for module in modules:
            res_msg = self.get_pro_module_status(domain, instance_id, module)
            self.info_list.append({"name": f"{modules[module]}({module})", "value": f"{res_msg}"})
        return self.code, self.error_msg, self.info_list, self.source_data


def health_check(params, assets, context_info):
    """健康检查"""

    # 服务地址，云防火墙openapi左上角可获取，不确定填实例值即可，如：cloudfw.aliyuncs.com
    service_address = assets["service_address"]
    # 区域ID，云防火墙openapi左上角可获取，不确定填实例值即可，如：cn-beijing
    domain_id = assets["domain_id"]
    # 平台获取的，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_id = assets["accesskey_id"]
    # 访问密钥，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_secret = assets["accesskey_secret"]

    # 返回值
    json_ret = {"code": 200, "msg": "", "data": {"records": "", "source_data": ""}}

    '''添加函数实现'''
    code, msg, info_list, source_data = AliyunWAF(
        service_address=service_address,
        domain_id=domain_id,
        accesskey_id=accesskey_id,
        accesskey_secret=accesskey_secret
    ).health_check_main()
    json_ret["data"]["records"] = info_list
    json_ret["data"]["source_data"] = source_data
    json_ret["code"] = code
    json_ret["msg"] = msg
    return json_ret


def get_domain_assets(params, assets, context_info):
    # 服务地址，云防火墙openapi左上角可获取，不确定填实例值即可，如：cloudfw.aliyuncs.com
    service_address = assets["service_address"]
    # 区域ID，云防火墙openapi左上角可获取，不确定填实例值即可，如：cn-beijing
    domain_id = assets["domain_id"]
    # 平台获取的，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_id = assets["accesskey_id"]
    # 访问密钥，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_secret = assets["accesskey_secret"]
    # 实例ID
    instance_id = assets["InstanceId"]

    # 返回值
    json_ret = {"code": 200, "msg": "", "data": {"records": "", "DomainNames": ""}}

    '''添加函数实现'''
    code, msg, info_list, source_data = AliyunWAF(
        service_address=service_address,
        domain_id=domain_id,
        accesskey_id=accesskey_id,
        accesskey_secret=accesskey_secret
    ).get_domain_assets_main(instance_id=instance_id)
    json_ret["data"]["records"] = info_list
    json_ret["data"]["source_data"] = source_data
    json_ret["code"] = code
    json_ret["msg"] = msg
    return json_ret


def modify_protection_module_status(params, assets, context_info):
    """实例开关"""
    # 服务地址，云防火墙openapi左上角可获取，不确定填实例值即可，如：cloudfw.aliyuncs.com
    service_address = assets["service_address"]
    # 区域ID，云防火墙openapi左上角可获取，不确定填实例值即可，如：cn-beijing
    domain_id = assets["domain_id"]
    # 平台获取的，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_id = assets["accesskey_id"]
    # 访问密钥，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_secret = assets["accesskey_secret"]
    #
    #
    domain = params["domain"]
    #
    module_status = params["ModuleStatus"]
    #
    instance_id = assets["InstanceId"]
    #
    defense_type = params["DefenseType"]
    # 返回值
    json_ret = {"code": 200, "msg": "", "data": {"code": "", "records": ""}}

    '''添加函数实现'''
    code, msg, info_list, source_data = AliyunWAF(
        service_address=service_address,
        domain_id=domain_id,
        accesskey_id=accesskey_id,
        accesskey_secret=accesskey_secret
    ).modify_protection_module_status_main(domain=domain,
                                           module_status=module_status,
                                           instance_id=instance_id,
                                           defense_type=defense_type
                                           )
    json_ret["data"]["records"] = info_list
    json_ret["data"]["source_data"] = source_data
    json_ret["data"]["code"] = code
    json_ret["msg"] = msg
    return json_ret


def describe_protection_module_rules(params, assets, context_info):
    """查询waf防护“黑名单”功能规则配置"""
    # 服务地址，云防火墙openapi左上角可获取，不确定填实例值即可，如：cloudfw.aliyuncs.com
    service_address = assets["service_address"]
    # 区域ID，云防火墙openapi左上角可获取，不确定填实例值即可，如：cn-beijing
    domain_id = assets["domain_id"]
    # 平台获取的，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_id = assets["accesskey_id"]
    # 访问密钥，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_secret = assets["accesskey_secret"]
    #
    #
    domain = params["domain"]
    #
    instance_id = assets["InstanceId"]

    # 返回值
    json_ret = {"code": 200, "msg": "", "data": {"code": "", "records": ""}}

    '''添加函数实现'''
    code, msg, info_list, source_data = AliyunWAF(
        service_address=service_address,
        domain_id=domain_id,
        accesskey_id=accesskey_id,
        accesskey_secret=accesskey_secret
    ).describe_protection_module_rules_main(domain=domain,
                                            instance_id=instance_id
                                            )
    json_ret["data"]["records"] = info_list
    json_ret["data"]["source_data"] = source_data
    json_ret["code"] = code
    json_ret["msg"] = msg
    return json_ret


def add_blackip(params, assets, context_info):
    """添加黑名单"""
    # 服务地址，云防火墙openapi左上角可获取，不确定填实例值即可，如：cloudfw.aliyuncs.com
    service_address = assets["service_address"]
    # 区域ID，云防火墙openapi左上角可获取，不确定填实例值即可，如：cn-beijing
    domain_id = assets["domain_id"]
    # 平台获取的，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_id = assets["accesskey_id"]
    # 访问密钥，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_secret = assets["accesskey_secret"]
    #
    domain = params["domain"]
    #
    instance_id = assets["InstanceId"]
    #
    blackip = params["blackip"]

    # 返回值
    json_ret = {"code": 200, "msg": "", "data": {"code": 200, "records": "", "source_data": "", "msg": ""}}

    '''添加函数实现'''
    code, msg, info_list, source_data = AliyunWAF(
        service_address=service_address,
        domain_id=domain_id,
        accesskey_id=accesskey_id,
        accesskey_secret=accesskey_secret
    ).add_blackip_main(domain=domain,
                       instance_id=instance_id,
                       blackip=blackip
                       )
    json_ret["data"]["records"] = info_list
    json_ret["data"]["source_data"] = source_data
    json_ret['data']['code'] = code
    json_ret['data']["msg"] = msg
    # json_ret["code"] = code
    # json_ret["msg"] = msg
    return json_ret


def remove_blackip(params, assets, context_info):
    """添加黑名单"""
    # 服务地址，云防火墙openapi左上角可获取，不确定填实例值即可，如：cloudfw.aliyuncs.com
    service_address = assets["service_address"]
    # 区域ID，云防火墙openapi左上角可获取，不确定填实例值即可，如：cn-beijing
    domain_id = assets["domain_id"]
    # 平台获取的，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_id = assets["accesskey_id"]
    # 访问密钥，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_secret = assets["accesskey_secret"]
    #
    domain = params["domain"]
    #
    instance_id = assets["InstanceId"]
    #
    blackip = params["blackip"]

    # 返回值
    json_ret = {"code": 200, "msg": "", "data": {"code": "", "records": "", "source_data": "", "code": 200, "msg": ""}}

    '''添加函数实现'''
    code, msg, info_list, source_data = AliyunWAF(
        service_address=service_address,
        domain_id=domain_id,
        accesskey_id=accesskey_id,
        accesskey_secret=accesskey_secret
    ).remove_blackip_main(domain=domain,
                          instance_id=instance_id,
                          blackip=blackip
                          )
    json_ret["data"]["records"] = info_list
    json_ret["data"]["source_data"] = source_data
    json_ret['data']['code'] = code
    json_ret['data']["msg"] = msg
    
    return json_ret


def get_pro_module_status(params, assets, context_info):
    """添加黑名单"""
    # 服务地址，云防火墙openapi左上角可获取，不确定填实例值即可，如：cloudfw.aliyuncs.com
    service_address = assets["service_address"]
    # 区域ID，云防火墙openapi左上角可获取，不确定填实例值即可，如：cn-beijing
    domain_id = assets["domain_id"]
    # 平台获取的，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_id = assets["accesskey_id"]
    # 访问密钥，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_secret = assets["accesskey_secret"]
    #
    domain = params["domain"]
    #
    instance_id = assets["InstanceId"]

    # 返回值
    json_ret = {"code": 200, "msg": "", "data": {"code": "", "records": ""}}

    '''添加函数实现'''
    code, msg, info_list, source_data = AliyunWAF(
        service_address=service_address,
        domain_id=domain_id,
        accesskey_id=accesskey_id,
        accesskey_secret=accesskey_secret
    ).get_pro_module_status_main(domain=domain,
                                 instance_id=instance_id
                                 )
    json_ret["data"]["records"] = info_list
    json_ret["data"]["source_data"] = source_data
    json_ret["code"] = code
    json_ret["msg"] = msg
    return json_ret


def add_whilelist(params, assets, context_info):
    """添加白名单"""
    # 服务地址，云防火墙openapi左上角可获取，不确定填实例值即可，如：cloudfw.aliyuncs.com
    service_address = assets["service_address"]
    # 区域ID，云防火墙openapi左上角可获取，不确定填实例值即可，如：cn-beijing
    domain_id = assets["domain_id"]
    # 平台获取的，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_id = assets["accesskey_id"]
    # 访问密钥，搜索【用户信息ID】可找到，如：LTAI5tR***vYVEmZ11
    accesskey_secret = assets["accesskey_secret"]
    #
    domain = params["domain"]
    #
    instance_id = assets["InstanceId"]
    #
    whileip = params["whileip"]
    #
    if_belong = params["if_belong"]

    # 返回值
    json_ret = {"code": 200, "msg": "", "data": {"code": "", "records": ""}}

    '''添加函数实现'''
    code, msg, info_list, source_data = AliyunWAF(
        service_address=service_address,
        domain_id=domain_id,
        accesskey_id=accesskey_id,
        accesskey_secret=accesskey_secret
    ).add_whilelist_main(domain=domain,
                         instance_id=instance_id,
                         whileip=whileip,
                         if_belong=if_belong
                         )
    json_ret["data"]["records"] = info_list
    json_ret["data"]["source_data"] = source_data
    json_ret["code"] = code
    json_ret["msg"] = msg
    return json_ret
