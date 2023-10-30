import warnings
import urllib3
import unittest
import tencent_wecom as wecom
from unittest import TestCase


warnings.filterwarnings("ignore")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Test(TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        warnings.simplefilter("ignore", UserWarning)
        warnings.simplefilter("ignore", DeprecationWarning)
        # 不知道谁的应用
        # assets = {
        #     "corp_id": "ww46ac1a9225c405df",
        #     "corp_secret": "AMqs9M27Jr3Cm2XrFJ4Q90CHsVdZql4UE9Z0s1ftvGs",
        #     "agent_id": 1000002,
        #     "to_user": "cai",
        # }
        # 通知应用-hp
        assets = {
            "corp_id": "ww5ff3a101f2931e08",
            "corp_id": "wx6c9ddf1ca1efaf4a",
            "corp_secret": "qnJiEVii_GYurUYGXU8oa0R3mfHtRdr7vQqwOaUX7Cc",
            "corp_secret": "8Z192IU5XBfcfAiw89MfXT0V7amdxMibXfadjIkwb6k",
            "agent_id": 1000002,
            "to_user": "YongHuZhengMang",
            "conn_time_out": 5,
            "verify_server_cert": False,
        }
        self.assets = assets
        self.context_info = {}

    @unittest.skip("跳过测试")
    def test_health_check(self):
        params = {
        }
        result = wecom.health_check(params, self.assets, self.context_info)
        print(result)

    @unittest.skip("跳过测试")
    def test_Send_Message(self):
        params = {
            "to_user": "cai",
            "content": "测试，请忽略",
        }
        result = wecom.Send_Message(params, self.assets, self.context_info)
        print(result)

    @unittest.skip("跳过测试")
    def test_get_user_device(self):
        params = {
            "to_user": "YongHuZhengMang",
            "type_device": 1,
        }
        result = wecom.Send_Message(params, self.assets, self.context_info)
        print(result)

    # @unittest.skip("跳过测试")
    def test_get_file_oper_record(self):
        params = {
            "to_user": "YongHuZhengMang",
            "type_device": 1,
            "timedelta": 1,
            "timedelta_unit": "minutes",
            "forward_time": "1",
            "start_time": "",
            "end_time": "",
            "limit": 1,
            "filter_file_type": 101,
        }
        result = wecom.get_file_oper_record(params, self.assets, self.context_info)
        print("test_get_file_oper_record: ", result)


if __name__ == "__main__":
    unittest.main()
