import unittest
import os
import requests

# 导入要测试的函数
from app_demo import rand_qinghua, read_file  # 请替换为正确的模块和函数名

class TestAppDemoFunctions(unittest.TestCase):

    def test_rand_qinghua(self):
        params = {}  # 设置合适的参数
        assets = {"timeout":10}  # 设置合适的参数
        context_info = {}  # 设置合适的参数

        result = rand_qinghua(params, assets, context_info)

        # 根据函数的预期行为编写断言
        self.assertEqual(result["code"], 200)  # 检查返回的code是否为200
        self.assertIn("msg", result)  # 检查返回结果中是否包含"msg"键

    def test_read_file(self):
        params = {"file": __file__}
        assets = {}  # 设置合适的参数
        context_info = {}  # 设置合适的参数

        result = read_file(params, assets, context_info)

        # 根据函数的预期行为编写断言
        self.assertEqual(result["code"], 200)  # 检查返回的code是否为200
        self.assertIn("content", result["data"])  # 检查返回结果中是否包含"data"中的"content"键

if __name__ == '__main__':
    unittest.main()
