import unittest
from unittest import TestCase
from unittest.main import main
import aliyun_waf


class Test(TestCase):
    """
    网络不可达；密码错误；Tftp未启动；   ——均已测试通过
    """

    def setUp(self):
        assets = {
            "service_address": "wafopenapi.ap-southeast-1.aliyuncs.com",
            "domain_id": "cn-hongkong",
            "accesskey_id": "",
            "accesskey_secret": "",
            "InstanceId": ""
        }
        self.assets = assets
        self.context_info = {}

    @unittest.skip("skip")
    def test_health_check(self):
        params = {}
        # 健康检查
        print(aliyun_waf.health_check(params, self.assets, self.context_info))

    @unittest.skip("skip")
    def test_get_domain_assets(self):
        params = {}
        # 获取域名资产信息
        print(aliyun_waf.get_domain_assets(params, self.assets, self.context_info))

    @unittest.skip("skip")
    def test_modify_protection_module_status(self):
        params = {
            "domain": "gl.honeypot.work",
            "ModuleStatus": 1,
            "DefenseType": "waf",
        }
        # 开关实例防护模块
        print(aliyun_waf.modify_protection_module_status(params, self.assets, self.context_info))

    @unittest.skip("skip")
    def test_describe_protection_module_rules(self):
        params = {
            "domain": "gl.honeypot.work",
        }
        # 查询waf防护“黑名单”功能规则配置
        print(aliyun_waf.describe_protection_module_rules(params, self.assets, self.context_info))

    @unittest.skip("skip")
    def test_add_blackip(self):
        params = {
            "domain": "gl.honeypot.work",
            "blackip": "65.0.0.1,65.0.0.2",
        }
        # 添加黑名单
        print(aliyun_waf.add_blackip(params, self.assets, self.context_info))

    @unittest.skip("skip")
    def test_remove_blackip(self):
        params = {
            "domain": "gl.honeypot.work",
            "blackip": "65.0.0.1,65.0.0.2",

        }
        # 移除黑名单
        print(aliyun_waf.remove_blackip(params, self.assets, self.context_info))

    @unittest.skip("skip")
    def test_get_pro_module_status(self):
        params = {
            "domain": "gl.honeypot.work",

        }
        # 查询WAF各防护功能的状态
        print(aliyun_waf.get_pro_module_status(params, self.assets, self.context_info))

    @unittest.skip("skip")
    def test_add_whilelist(self):
        params = {
            "domain": "gl.honeypot.work",
            "whileip": "65.0.0.1,65.0.0.2/24,65.0.0.3",
            "if_belong": 0
        }
        # 新增IP白名单
        print(aliyun_waf.add_whilelist(params, self.assets, self.context_info))


if __name__ == "__main__":
    # unittest.main(defaultTest='suite')
    unittest.main()
