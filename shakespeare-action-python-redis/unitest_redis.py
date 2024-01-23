#coding:utf-8

import unittest
import redis_client
class Test(unittest.TestCase):
    assets = {
        "host": "192.168.44.2",
        "password": "qwe123"
    }
    
    # @unittest.skip("注释本行即测试")
    def test_llen(self):
        params = {
            "key": "honeyguide_redis_llen_test",
            "value": "wuzhizhineng"
        }
        redis_client.redis_del(params, self.assets, None)
        redis_client.redis_lpush(params, self.assets, None)
        
        result = redis_client.redis_llen(params, self.assets, None)
        self.assertEqual(result["data"]["length"], 1, "REDIS LLEN")

        redis_client.redis_del(params, self.assets, None)
        
        result = redis_client.redis_llen(params, self.assets, None)
        self.assertEqual(result["data"]["length"], 0, "REDIS LLEN")

    # @unittest.skip("注释本行即测试")
    def test_key_exists_del(self):
        params = {
            "key": "honeyguide_redis_exists_del_test",
            "value": "wuzhizhineng"
        }
        redis_client.redis_set(params, self.assets, None)
        result = redis_client.redis_exists(params, self.assets, None)
        self.assertEqual(result["data"]["exists"], True, "REDIS EXISTS")

        result = redis_client.redis_del(params, self.assets, None)
        self.assertEqual(result["data"]["success"], True, "REDIS DEL")

        result = redis_client.redis_exists(params, self.assets, None)
        self.assertEqual(result["data"]["exists"], False, "REDIS EXISTS")


    # @unittest.skip("注释本行即测试")
    def test_get_set(self):
        params = {
            "key": "honeyguide_redis_get_set_test",
            "value": "wuzhizhineng"
        }
        result = redis_client.redis_set(params, self.assets, None)
        self.assertEqual(result["data"]["success"], True, "REDIS SET")
        
        result = redis_client.redis_get(params, self.assets, None)
        self.assertEqual(result["data"]["value"], "wuzhizhineng", "REDIS GET")

    # @unittest.skip("注释本行即测试")
    def test_lpush_rpop(self):
        params = {
            "key": "honeyguide_redis_lpush_rpop_test",
            "value": "wuzhizhineng"
        }
        result = redis_client.redis_lpush(params, self.assets, None)
        self.assertEqual(result["data"]["success"], True, "REDIS LPUSH")

        result = redis_client.redis_rpop(params, self.assets, None)
        self.assertEqual(result["data"]["value"], "wuzhizhineng", "REDIS RPOP")

    # @unittest.skip("注释本行即测试")
    def test_raw_command(self):
        params = {
            "command": "llen honeyguide_redis_llen_test"
        }
        result = redis_client.redis_raw_command(params, self.assets, None)
        self.assertEqual(result["summary"]["statusCode"], 200, "REDIS Raw Command")

if __name__ == '__main__':
    # python unitest_redis.py -v
    unittest.main()