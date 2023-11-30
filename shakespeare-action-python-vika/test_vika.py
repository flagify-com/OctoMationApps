import json
import sys
import unittest

import vika


class Test_vika(unittest.TestCase):

    def setUp(self):
        self.assets = {"host": "https://api.vika.cn",
                       "api_token": "**************",
                       "space_id": "**************",
                       "datasheetId": '**************'
                       }
        self.context_info = {}

    def tearDown(self):
        print("----------> Test Done! <----------\n")

    def test_space(self):
        # 健康检查
        print('---------- Start {} ------------'.format(sys._getframe().f_code.co_name))
        res = vika.spaces({}, self.assets, self.context_info)
        print(res)

    def test_search_tables(self):
        print('---------- Start {} ------------'.format(sys._getframe().f_code.co_name))

        params = {
            # "filterByFormula": "管理员审批",
            # "filterByFormula":'{管理员审批}="同意"'
            # "filterByFormula":'AND({管理员审批}="同意",{扫描进度}="扫描完成")'
            # "filterByFormula":'AND({管理员审批}="同意",{扫描进度}=BLANK())'
            # "filterByFormula":'{管理员审批}="拒绝"'
            # "filterByFormula":'{管理员审批}=BLANK()'
            # "filterByFormula":'{扫描进度}="接收事件"'
            # "filterByFormula": '{序号}=6'
            # "filterByFormula": '{状态}=“进行中”&&{vika_notify}=BLANK()'
            # "filterByFormula": '{需填报人}!=BLANK()'
            # "filterByFormula": '{状态}=“进行中”&&{需填报人}!=BLANK()&&{vika_notify}=BLANK()'
        }
        res = vika.search_tables(params, self.assets, self.context_info)
        print(json.dumps(res, ensure_ascii=False))

    def test_change_tables(self):
        print('---------- Start {} ------------'.format(sys._getframe().f_code.co_name))

        params = {
            # "col_name": "soar_status",
            # "value": "已处理"
            "recordId": "recMkRaklU3Vq",
            "col_name": "扫描结果",
        }
        res = vika.change_tables(params, self.assets, self.context_info)


if __name__ == '__main__':
    unittest.main(verbosity=1)
