# coding: utf-8
from hillstonenet_ti import detail_url, detail_ip, detail_domain,detail_file
import unittest
import time
import random

class TestHillstonenetTi(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.assets = {
            "api_key": "6d419c77d0539109cc9fc4ec3fc92993e6f41babd0685929c0c449b321ad5a68", 
            "api_domain": "ti.hillstonenet.com.cn"
        }
        self.params = {
            "ip": "184.32.167.72",
            "domain": "github.com",
            "url": "https://github.com/",
            "file_hash": "02cfbb7326fd467f87a810921cfebe9e"
        }
    def test_detail_url(self):
        time.sleep(random.randint(10, 60))
        ret = detail_url(self.params, self.assets, None)
        self.assertEqual(ret['data']['err_code'], 0)

    def test_detail_ip(self):
        time.sleep(random.randint(10, 60))
        ret = detail_ip(self.params, self.assets, None)
        self.assertEqual(ret['data']['err_code'], 0)

    def test_detail_domain(self):
        time.sleep(random.randint(10, 60))
        ret = detail_domain(self.params, self.assets, None)
        self.assertEqual(ret['data']['err_code'], 0)

    def test_detail_file(self):
        time.sleep(random.randint(10, 60))
        ret = detail_file(self.params, self.assets, None)
        self.assertEqual(ret['data']['err_code'], 0)


if __name__ == '__main__':
    print("\n防止并发导致接口调用触发频次限制，随机延时1-10秒")
    unittest.main()