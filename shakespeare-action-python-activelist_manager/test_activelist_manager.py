import unittest
from activelist_manager import clear_active_list, initialize_active_list_table, add_record_to_active_list, count_records_within_time_window, list_all_active_lists, remove_record_from_active_list, health_check,delete_active_list
from unittest import TestCase
import time
# 注释对应的@unittest.skip("skipping ...")装饰器，以启动单元测试

class TestActiveListManager(TestCase):
    
    @unittest.skip("skipping test_clear_active_list_success")
    def test_02_initialize_active_list_table_success(self):
        assets = {}
        params = {"activelist_name": "test_activelist"}
        context = {}
        json_ret =initialize_active_list_table(params, assets,context)   # This function creates the active_list table in the database if it doesn't exist.
        print(json_ret["data"]['err_msg'])
        self.assertEqual(json_ret["data"]["err_code"], 0)

    @unittest.skip("skipping test_clear_active_list_success")
    def test_03_add_record_to_active_list(self):
        assets = {}
        params = {
            "activelist_name": "test_activelist" 
        }
        context = {}

        ## 清空活动列表
        json_ret = clear_active_list(params, assets, context)
        print(json_ret['data']['err_msg'])

        # 查看表中记录数量
        params = {
            "activelist_name": "test_activelist",
            "item_key": "test_key_1"
        }
        json_ret = count_records_within_time_window(params, assets, context)
        print(json_ret["data"]['err_msg'])
        self.assertEqual(json_ret["data"]["record_count"], 0)

        # 添加一条记录
        params = {
            "activelist_name": "test_activelist",
            "item_key": "test_key_1",
            "item_value": "test_key_1_value_1",
            "item_remark": "test_key_1_remark_1"
        }
        json_ret1 = add_record_to_active_list(params, assets, context)
        print(json_ret1["data"]['err_msg'])
        self.assertEqual(json_ret1["data"]["err_code"], 0)
        
        # 添加一条记录，key相同，value不同，插入一条新记录

        params = {
            "activelist_name": "test_activelist",
            "item_key": "test_key_1",
            "item_value": "test_key_1_value_2",
            "item_remark": "test_key_1_remark_2"
        }
        json_ret1 = add_record_to_active_list(params, assets,context)
        print(json_ret1["data"]['err_msg'])
        self.assertEqual(json_ret1["data"]["err_code"], 0)
        
        json_ret3 = count_records_within_time_window(params, assets, context)
        print(json_ret3["data"]['err_msg'])
        self.assertEqual(json_ret3["data"]["record_count"], 2)
    
    @unittest.skip("skipping test_add_record_to_active_list_replace")
    def test_04_add_record_to_active_list_replace(self):
        """
        测试添加记录时，如果记录已经存在，是否会被替换
        """
        assets = {}
        params = {
            "activelist_name": "test_activelist" 
        }
        context = {}

        ## 清空活动列表
        json_ret = clear_active_list(params, assets, context)
        print(json_ret['data']['err_msg'])
        
        # 查看表中记录数量
        params = {
            "activelist_name": "test_activelist",
            "item_key": "test_key_1"
        }
        json_ret = count_records_within_time_window(params, assets, context)
        print(json_ret["data"]['err_msg'])
        self.assertEqual(json_ret["data"]["record_count"], 0)

        # 添加一条记录
        params = {
            "activelist_name": "test_activelist",
            "item_key": "test_key_1",
            "item_value": "test_key_1_value_1",
            "item_remark": "test_key_1_remark_1",
            "replace_if_exists": True
        }
        json_ret1 = add_record_to_active_list(params, assets, context)
        print(json_ret1["data"]['err_msg'])
        self.assertEqual(json_ret1["data"]["err_code"], 0)
        
        # 添加一条记录，但key相同，value不同，应该会替换掉原记录

        params = {
            "activelist_name": "test_activelist",
            "item_key": "test_key_1",
            "item_value": "test_key_1_value_2",
            "item_remark": "test_key_1_remark_2",
            "replace_if_exists": True
        }
        json_ret1 = add_record_to_active_list(params, assets,context)
        print(json_ret1["data"]['err_msg'])
        self.assertEqual(json_ret1["data"]["err_code"], 0)
        
        json_ret3 = count_records_within_time_window(params, assets, context)
        print(json_ret3["data"]['err_msg'])
        self.assertEqual(json_ret3["data"]["record_count"], 1)

    @unittest.skip("skipping test_count_records_within_time_window")
    def test_05_list_all_active_lists(self):
        """
        列举出所有active_list活动列表（_al_开头的表）
        """
        assets = {}
        params = {}
        context = {}

        ## 清空活动列表
        json_ret = list_all_active_lists(params, assets, context)
        print(json_ret['data']['activelists'])
        self.assertEqual(json_ret['data']['err_code'], 0)

    @unittest.skip("skipping test_remove_record_from_active_list")
    def test_06_delete_active_list(self):
        """
        删除活动列表
        """
        assets = {}
        params = {"activelist_name": "test_activelist"}
        context = {}

        ## 删除活动列表
        json_ret = delete_active_list(params, assets, context)
        print(json_ret['data']['err_msg'])
        self.assertEqual(json_ret['data']['err_code'], 0)

    # @unittest.skip("skipping test_health_check")
    def test_01_health_check(self):
        assets = {}
        params = {"activelist_name": "test_activelist"}
        context = {}
        json_ret = health_check(params, assets, context)
        print(json_ret["summary"]["msg"])
        self.assertEqual(json_ret["summary"]["statusCode"], 200)

if __name__ == '__main__':
    unittest.main()