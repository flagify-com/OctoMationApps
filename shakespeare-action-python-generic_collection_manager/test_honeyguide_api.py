import unittest
from hg_api import HoneyGuideAPI
import logging

logging.basicConfig(level=logging.INFO)

collection_id = 0

class TestHoneyguideAPI(unittest.TestCase):
    def setUp(self) -> None:
        self._hg_api_url = "https://hg.wuzhi-ai.com"
        self._hg_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.***.y7voPwo3qeuVqfLuFGIL3xmmPzkgU_Rd4fBFeX41fiE"
        self._context_info ={
            "appName": "generic_collection_manager", 
            "actionName": "UniTest:TestGenericCollectionManager", 
            "eventId": "231", 
            "activieId": "2312", 
            "logMode": False
        }
        self._hg_api = HoneyGuideAPI(self._hg_api_url, self._hg_token,self._context_info)
        
    def test_create_generic_collection(self):
        collection_name = "unitest_collection_name_202408"
        collection_name_cn = "单元测试集合202408"
        collection_description = "单元测试函数test_create_generic_collection()"
        collection_id_1 = self._hg_api.create_generic_collection(collection_name, collection_name_cn, collection_description)
        self.assertGreater(collection_id_1, 0)
        global collection_id
        collection_id = collection_id_1

        # 创建重复的集合
        collection_id_2 = self._hg_api.create_generic_collection(collection_name, collection_name_cn, collection_description)
        self.assertEqual(collection_id_2, collection_id_1)
        self.assertEqual(self._hg_api.summary["statusCode"], 0)

    def test_get_generic_collections(self):
        # 获取所有通用集合，一页10个，最多17个
        collections = self._hg_api.get_generic_collections(batch_size=10,max_count=17)
        self.assertEqual(self._hg_api.summary["statusCode"], 0)
        self.assertGreaterEqual(len(collections), 1)
        unitest_collection_name_found = False        
        for collection in collections:
            if collection['name'].startswith("unitest_collection_name"):
                unitest_collection_name_found = True
                break
        self.assertTrue(unitest_collection_name_found)

    def test_delete_generic_collection_by_id(self):
        global collection_id
        logging.info(f"Collection id to delete: {collection_id}")
        delete_collection_result = self._hg_api.delete_generic_collection_by_id(collection_id)
        logging.info(self._hg_api.summary)
        self.assertEqual(delete_collection_result, True)
        # 尝试删除不存在的集合
        delete_collection_result = self._hg_api.delete_generic_collection_by_id(0)
        logging.info(delete_collection_result)
        logging.info(self._hg_api.summary)
        self.assertEqual(delete_collection_result, True)

    def test_add_generic_collection_element(self):
        collection_name = "unitest_collection_name_202408"
        element_value = "unitest_element_value_202408_element_1"
        element_remark = "unitest_element_value_202408_element_1:test_add_collection_element()"

        # 添加一个集合元素
        add_element_result = self._hg_api.add_generic_collection_element(collection_name=collection_name, element_value=element_value, element_remark=element_remark)
        logging.info(f"add_element_result: {self._hg_api.summary}")
        self.assertTrue(add_element_result)

        # 添加重复的集合元素
        add_element_result = self._hg_api.add_generic_collection_element(collection_name=collection_name, element_value=element_value, element_remark=element_remark)
        logging.info(f"add_element_result: {self._hg_api.summary}")
        self.assertTrue(add_element_result)

        logging.info(f"再添加19个元素，请稍等...")
        # 添加另一个集合元素
        for i in range(2, 21):
            element_value = f"unitest_element_value_202408_element_{i}"
            element_remark = f"unitest_element_value_202408_element_{i}:test_add_collection_element()"
            logging.info(f"添加元素{i}: {element_value}")
            add_element_result = self._hg_api.add_generic_collection_element(collection_name=collection_name, element_value=element_value, element_remark=element_remark)

    def test_check_generic_collection_element_exists(self):
        element_exists = self._hg_api.check_generic_collection_element_exists(collection_name="unitest_collection_name_202408", element_value="unitest_element_value_202408_element_1")
        logging.info(self._hg_api.summary)
        self.assertTrue(element_exists)
        element_exists = self._hg_api.check_generic_collection_element_exists(collection_name="unitest_collection_name_202408", element_value="unitest_element_value_202408_element_NOT_EXIST")
        logging.info(self._hg_api.summary)
        self.assertFalse(element_exists)

    def test_get_generic_collection_elements(self):
        # 返回通用集合的元素，并输出为字典组成的数组，查询方式：一页4个，最多13个
        collection_name="unitest_collection_name_202408"
        elements = self._hg_api.get_generic_collection_elements(collection_name=collection_name, batch_size=4, max_count=13)
        self.assertEqual(self._hg_api.summary["statusCode"], 0)
        self.assertEqual(len(elements), 13)

    def test_update_generic_collection_element(self):
        collection_name = "unitest_collection_name_202408"
        element_value = "unitest_element_value_202408_element_1"
        element_remark= "test_update_collection_element:updated_remark"

        update_element_result = self._hg_api.update_generic_collection_element_by_value(collection_name=collection_name, element_value=element_value, element_remark=element_remark)
        logging.info(self._hg_api.summary)
        self.assertTrue(update_element_result)

        # 尝试更新不存在的元素
        element_value = "unitest_element_value_202408_element_NOT_EXIST"
        update_element_result = self._hg_api.update_generic_collection_element_by_value(collection_name=collection_name, element_value=element_value, element_remark=element_remark)
        logging.info(self._hg_api.summary)
        self.assertFalse(update_element_result)

    def test_delete_generic_collection_element_by_name(self):
        collection_name = "unitest_collection_name_202408"
        element_value = "unitest_element_value_202408_element_5"
        delete_element_result = self._hg_api.delete_generic_collection_element_by_name(collection_name=collection_name, element_value=element_value)
        logging.info(self._hg_api.summary)
        self.assertTrue(delete_element_result)

        # 重复删除，尝试删除不存在的元素
        delete_element_result = self._hg_api.delete_generic_collection_element_by_name(collection_name=collection_name, element_value=element_value)
        logging.info(self._hg_api.summary)
        self.assertTrue(delete_element_result)



if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestHoneyguideAPI('test_create_generic_collection'))
    suite.addTest(TestHoneyguideAPI('test_get_generic_collections'))
    suite.addTest(TestHoneyguideAPI('test_add_generic_collection_element'))
    suite.addTest(TestHoneyguideAPI('test_check_generic_collection_element_exists'))
    suite.addTest(TestHoneyguideAPI('test_get_generic_collection_elements'))
    suite.addTest(TestHoneyguideAPI('test_update_generic_collection_element'))
    suite.addTest(TestHoneyguideAPI('test_delete_generic_collection_by_id'))
    runner = unittest.TextTestRunner()
    runner.run(suite)