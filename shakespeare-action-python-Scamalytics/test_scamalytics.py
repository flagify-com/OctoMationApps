#coding: utf-8
import unittest
from scamalytics import get_ip_fraud_risk_info, health_check

class TestScamalytics(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.assets = {
            "api_user": "flagify",
            "api_key": "52bbb36c0be7f03b0727fd6ca45e76d20872999aeac43ce83d6abbd636439770"
        }

    # @unittest.skip("skip")
    def test_lan_ip(self):
        params = {
            "ip": "192.168.127.12"
        }
        risk_info = get_ip_fraud_risk_info(params, self.assets, None)
        self.assertEqual(risk_info['data']['isp_name'], 'Private network')

    # @unittest.skip("skip")
    def test_cn_home_ip(self):
        params = {
            "ip": "222.67.207.4"
        }
        risk_info = get_ip_fraud_risk_info(params, self.assets, None)
        self.assertEqual(risk_info['data']['ip_state_name'], 'Shanghai')
    
    # @unittest.skip("skip")
    def test_hk_server_ip(self):
        params = {
            "ip": "119.28.82.185"
        }
        risk_info = get_ip_fraud_risk_info(params, self.assets, None)
        self.assertTrue(risk_info['data']['server'])

    # @unittest.skip("skip")
    def test_proxy_ip(self):
        params = {
            "ip": "216.58.194.174"
        }
        risk_info = get_ip_fraud_risk_info(params, self.assets, None)
        self.assertGreater(risk_info['data']['score'], 0)

    # @unittest.skip("skip")
    def test_get_ip_fraud_risk_without_api_key(self):
        assets = {}
        params = {
            "ip": "216.58.194.174"
        }
        risk_info = get_ip_fraud_risk_info(params, assets, None)
        self.assertEqual(risk_info['data']['err_code'], 0)

    # @unittest.skip("skip")
    def test_health_check(self):
        params= {}
        assets = {}
        risk_info = health_check(params, assets, None)
        self.assertEqual(risk_info['summary']['statusCode'], 200)
        risk_info = health_check(params, self.assets, None)
        self.assertEqual(risk_info['summary']['statusCode'], 200)

if __name__ == '__main__':
    unittest.main()