import unittest
from generic_collection_manager import list_generic_collections, create_generic_collection, delete_generic_collection
from generic_collection_manager import list_generic_collection_elements, add_generic_collection_item,get_generic_collection_element_info
from generic_collection_manager import update_generic_collection_element, delete_generic_collection_element
from generic_collection_manager import check_generic_collection_element_exists, health_check
import logging
logging.basicConfig(level=logging.INFO)

class TestGenericCollectionManager(unittest.TestCase):
    def setUp(self):
        self._hg_api_url = "https://hg.wuzhi-ai.com"
        # self._hg_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.***.y7voPwo3qeuVqfLuFGIL3xmmPzkgU_Rd4fBFeX41fiE"
        self._hg_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJiYWJhb3pob3UiLCJzdWIiOiJPcGVuQVBJIG9mIHd1emhpLWFpLmNvbSIsImFwcElkIjoxMTI0OTQ1OTk4MTkxNjI2MywiaXNzIjoid3V6aGktYWkuY29tIiwiaWF0IjoxNzIzNTE2MzU4fQ.y7voPwo3qeuVqfLuFGIL3xmmPzkgU_Rd4fBFeX41fiE"
        self._timeout_seconds = 10
        self._context_info ={
            "appName": "generic_collection_manager", 
            "actionName": "UniTest:TestGenericCollectionManager", 
            "eventId": "231", 
            "activieId": "2312", 
            "logMode": False
        }
        print(self._context_info)

    def test_health_check(self):
        assets = {
            "hg_host": self._hg_api_url,
            "hg_token": self._hg_token,
            "timeout_seconds": self._timeout_seconds
        }
        params = {}
        context_info = self._context_info
        result = health_check(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 200)

    def test_create_generic_collection(self):
        assets = {
            "hg_host": self._hg_api_url,
            "hg_token": self._hg_token,
            "timeout_seconds": self._timeout_seconds
        }
        
        context_info = self._context_info
        collection_name = "unitest_collection_name_20240825_1"
        collection_cnname = "单元测试集合20240825_1"
        collection_description = "单元测试函数:test_create_generic_collection()"
        params = {
            "collection_name": collection_name,
            "collection_cnname": collection_cnname,
            "collection_description": collection_description
        }
        result = create_generic_collection(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertGreater(result["data"]["collection_id"], 0)

        # 重复创建集合
        result = create_generic_collection(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertTrue(result["data"]["duplicated"])

        # 多创建几个集合
        logging.info("开始创建多个集合，耐心等待...")
        for i in range(2, 21):
            collection_name = "unitest_collection_name_20240825_{}".format(i)
            collection_cnname = "单元测试集合20240825_{}".format(i)
            collection_description = "单元测试函数:test_create_generic_collection()_{}".format(i)
            params = {
                "collection_name": collection_name,
                "collection_cnname": collection_cnname,
                "collection_description": collection_description
            }
            result = create_generic_collection(params, assets, context_info)
            logging.info(result)
        
        
    def test_list_generic_collections(self):
        assets = {
            "hg_host": self._hg_api_url,
            "hg_token": self._hg_token,
            "timeout_seconds": self._timeout_seconds
        }
        params = {
            "batch_size": 5,
            "max_count": 17
        }
        context_info = self._context_info
        result = list_generic_collections(params, assets, context_info)
        logging.debug(result)
        self.assertEqual(result['data']['count'], 17)


    def test_delete_generic_collection(self):
        assets = {
            "hg_host": self._hg_api_url,
            "hg_token": self._hg_token,
            "timeout_seconds": self._timeout_seconds
        }
        params = {
            "collection_name": "unitest_collection_name_20240825_1"
        }
        context_info = self._context_info
        result = delete_generic_collection(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 0)
        # 多删除几个集合
        logging.info("开始删除多个集合，耐心等待...")
        for i in range(2, 21):
            collection_name = "unitest_collection_name_20240825_{}".format(i)
            params = {
                "collection_name": collection_name
            }
            result = delete_generic_collection(params, assets, context_info)
            logging.info(result)
            self.assertEqual(result["summary"]["statusCode"], 0)

    def test_add_generic_collection_item(self):
        assets = {
            "hg_host": self._hg_api_url,
            "hg_token": self._hg_token,
            "timeout_seconds": self._timeout_seconds
        }
        params = {
            "collection_name": "unitest_collection_name_20240825_1",
            "element_value": "unitest_element_value_20240825_1",
            "element_cnname": "单元测试元素_20240825_1",
            "element_remark": "单元测试函数:test_add_generic_collection_item()",
        }
        context_info = self._context_info
        result = add_generic_collection_item(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 0)
        
        # 重复添加元素
        result = add_generic_collection_item(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertTrue(result["data"]["duplicated"])

        # 再添加几个元素
        logging.info("开始添加多个元素，耐心等待...")
        for i in range(2, 21):
            element_value = "unitest_element_value_20240825_{}".format(i)
            element_remark = "单元测试函数:test_add_generic_collection_item()_{}".format(i)
            params = {
                "collection_name": "unitest_collection_name_20240825_1",
                "element_value": element_value,
                "element_remark": element_remark
            }
            result = add_generic_collection_item(params, assets, context_info)
            logging.info(result)
            self.assertEqual(result["summary"]["statusCode"], 0)

    def test_list_generic_collection_elements(self):
        assets = {
            "hg_host": self._hg_api_url,
            "hg_token": self._hg_token,
            "timeout_seconds": self._timeout_seconds
        }
        params = {
            "collection_name": "unitest_collection_name_20240825_1",
            "batch_size": 5,
            "max_count": 17
        }
        context_info = self._context_info
        result = list_generic_collection_elements(params, assets, context_info)
        logging.debug(result)
        self.assertEqual(result['data']['count'], 17)

    def test_update_generic_collection_element(self):
        assets = {
            "hg_host": self._hg_api_url,
            "hg_token": self._hg_token,
            "timeout_seconds": self._timeout_seconds
        }
        params = {
            "collection_name": "unitest_collection_name_20240825_1",
            "element_value":   "unitest_element_value_20240825_2",
            "element_remark":  "单元测试函数:test_update_generic_collection_element(),updated",
        }
        context_info = self._context_info
        result = update_generic_collection_element(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 0)

        # 更新不存在的元素
        params = {
            "collection_name": "unitest_collection_name_20240825_1",
            "element_value":   "unitest_element_value_20240825_2_NOT_EXIST",
            "element_remark":  "单元测试函数:test_update_generic_collection_element(),updated",
        }
        context_info = self._context_info
        result = update_generic_collection_element(params, assets, context_info)
        logging.info(result)
        self.assertNotEqual(result["summary"]["statusCode"], 0)

    def test_get_generic_collection_element_info(self):
        assets = {
            "hg_host": self._hg_api_url,    
            "hg_token": self._hg_token,
            "timeout_seconds": self._timeout_seconds
        }
        params = {
            "collection_name": "unitest_collection_name_20240825_1",
            "element_value": "unitest_element_value_20240825_1"
        }
        context_info = self._context_info
        result = get_generic_collection_element_info(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertGreater(result["data"]["id"], 0)

        # 查看不存在的元素信息
        params = {
            "collection_name": "unitest_collection_name_20240825_1",
            "element_value": "unitest_element_value_20240825_1_NOT_EXIST"
        }
        context_info = self._context_info
        result = get_generic_collection_element_info(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertEqual(result["data"]["id"], 0)

    def test_check_generic_collection_element_exists(self):
        assets = {
            "hg_host": self._hg_api_url,
            "hg_token": self._hg_token,
            "timeout_seconds": self._timeout_seconds    
        }
        params = {
            "collection_name": "unitest_collection_name_20240825_1",
            "element_value": "unitest_element_value_20240825_2"
        }
        # params = {
        #     "collection_name": "unitest_collection_name_20240825",
        #     "element_value": "121"
        # }
        context_info = self._context_info
        result = check_generic_collection_element_exists(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertTrue(result["data"]["element_exists"])

        # 元素不存在
        params = {
            "collection_name": "unitest_collection_name_20240825_1",
            "element_value": "not_exist_element_name_20240825_2"
        }
        result = check_generic_collection_element_exists(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 404)
        self.assertFalse(result["data"]["element_exists"])



    def test_delete_generic_collection_element(self):
        assets = {
            "hg_host": self._hg_api_url,
            "hg_token": self._hg_token,
            "timeout_seconds": self._timeout_seconds
        }
        params = {
            "collection_name": "unitest_collection_name_20240825_1",
            "element_value": "unitest_element_value_20240825_1"
        }
        context_info = self._context_info
        result = delete_generic_collection_element(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 0)

        # 删除不存在的元素
        result = delete_generic_collection_element(params, assets, context_info)
        logging.info(result)
        self.assertEqual(result["summary"]["statusCode"], 0)

        # 再删除几个元素
        logging.info("开始删除多个元素，耐心等待...")
        for i in range(2, 21):
            element_value = "unitest_element_value_20240825_{}".format(i)
            params = {
                "collection_name": "unitest_collection_name_20240825_1",
                "element_value": element_value
            }
            result = delete_generic_collection_element(params, assets, context_info)
            logging.info(result)
            self.assertEqual(result["summary"]["statusCode"], 0)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestGenericCollectionManager('test_health_check'))
    # 集合操作
    suite.addTest(TestGenericCollectionManager('test_create_generic_collection'))
    suite.addTest(TestGenericCollectionManager('test_list_generic_collections'))
    # 元素操作
    suite.addTest(TestGenericCollectionManager('test_add_generic_collection_item'))
    suite.addTest(TestGenericCollectionManager('test_list_generic_collection_elements'))
    suite.addTest(TestGenericCollectionManager('test_update_generic_collection_element'))
    suite.addTest(TestGenericCollectionManager('test_check_generic_collection_element_exists'))
    suite.addTest(TestGenericCollectionManager('test_get_generic_collection_element_info'))
    # 元素操作：清理
    suite.addTest(TestGenericCollectionManager('test_delete_generic_collection_element'))
    # 集合操作：清理
    suite.addTest(TestGenericCollectionManager('test_delete_generic_collection'))
    runner = unittest.TextTestRunner()
    runner.run(suite)