# -*- coding: utf-8 -*-


def set_variable(params, assets, context_info):
    """设置变量"""

    
    iv_str_01= ""
    if "iv_str_01" in params.keys() and params["iv_str_01"] != "" and params["iv_str_01"] is not None:
        iv_str_01= params["iv_str_01"]

    # 输入：字符型变量01
    iv_str_01 = "" if "iv_str_01" not in params.keys() or params["iv_str_01"] is None else params["iv_str_01"]
    # 输入：字符型变量01的label
    iv_str_01_label = "" if "iv_str_01_label" not in params.keys() or params["iv_str_01_label"] is None else params["iv_str_01_label"]
    
    # 输入：字符型变量02
    iv_str_02 = "" if "iv_str_02" not in params.keys() or params["iv_str_02"] is None else params["iv_str_02"]
    # 输入：字符型变量02的label
    iv_str_02_label = "" if "iv_str_02_label" not in params.keys() or params["iv_str_02_label"] is None else params["iv_str_02_label"]
    
    # 输入：字符型变量03
    iv_str_03 = "" if "iv_str_03" not in params.keys() or params["iv_str_03"] is None else params["iv_str_03"]
    # 输入：字符型变量03的label
    iv_str_03_label = "" if "iv_str_03_label" not in params.keys() or params["iv_str_03_label"] is None else params["iv_str_03_label"]
    
    # 输入：字符型变量04
    iv_str_04 = "" if "iv_str_04" not in params.keys() or params["iv_str_04"] is None else params["iv_str_04"]
    # 输入：字符型变量04的label
    iv_str_04_label = "" if "iv_str_04_label" not in params.keys() or params["iv_str_04_label"] is None else params["iv_str_04_label"]
    
    # 输入：字符型变量05
    iv_str_05 = "" if "iv_str_05" not in params.keys() or params["iv_str_05"] is None else params["iv_str_05"]
    # 输入：字符型变量05的label
    iv_str_05_label = "" if "iv_str_05_label" not in params.keys() or params["iv_str_05_label"] is None else params["iv_str_05_label"]
    
    # 输入：字符型变量06
    iv_str_06 = "" if "iv_str_06" not in params.keys() or params["iv_str_06"] is None else params["iv_str_06"]
    # 输入：字符型变量06的label
    iv_str_06_label = "" if "iv_str_06_label" not in params.keys() or params["iv_str_06_label"] is None else params["iv_str_06_label"]
    

    
    # 输入：整型变量01
    iv_int_01 = 0 if "iv_int_01" not in params.keys() or params["iv_int_01"] is None else int(params["iv_int_01"])
    # 输入：整型变量01的label
    iv_int_01_lable = "" if "iv_int_01_lable" not in params.keys() or params["iv_int_01_lable"] is None else params["iv_int_01_lable"]
    
    # 输入：整型变量02
    iv_int_02 = 0 if "iv_int_02" not in params.keys() or params["iv_int_02"] is None else int(params["iv_int_02"])
    # 输入：整型变量02的label
    iv_int_02_lable = "" if "iv_int_02_lable" not in params.keys() or params["iv_int_02_lable"] is None else params["iv_int_02_lable"]

    # 输入：整型变量03
    iv_int_03 = 0 if "iv_int_03" not in params.keys() or params["iv_int_03"] is None else int(params["iv_int_03"])
    # 输入：整型变量03的label
    iv_int_03_lable = "" if "iv_int_03_lable" not in params.keys() or params["iv_int_03_lable"] is None else params["iv_int_03_lable"]

    

    # 输入：双精度浮点型变量01
    iv_double_01 = 0 if "iv_double_01" not in params.keys() or params["iv_double_01"] is None else float(params["iv_double_01"])
    # 输入：双精度浮点型变量01的label
    iv_double_01_lable = "" if "iv_double_01_lable" not in params.keys() or params["iv_double_01_lable"] is None else params["iv_double_01_lable"]

    # 输入：双精度浮点型变量02
    iv_double_02 = 0 if "iv_double_02" not in params.keys() or params["iv_double_02"] is None else float(params["iv_double_02"])
    # 输入：双精度浮点型变量02的label
    iv_double_02_lable = "" if "iv_double_02_lable" not in params.keys() or params["iv_double_02_lable"] is None else params["iv_double_02_lable"]

    # 输入：布尔型变量01
    iv_bool_01 = False if "iv_bool_01" not in params.keys() or params["iv_bool_01"] is None else bool(params["iv_bool_01"])
    # 输入：布尔型变量01的label
    iv_bool_01_label = "" if "iv_bool_01_label" not in params.keys() or params["iv_bool_01_label"] is None else params["iv_bool_01_label"]
    
    # 返回值
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "ov_str_01": iv_str_01,
            "ov_str_01_label": iv_str_01_label,
            "ov_str_02": iv_str_02,
            "ov_str_02_label": iv_str_02_label,
            "ov_str_03": iv_str_03,
            "ov_str_03_label": iv_str_03_label,
            "ov_str_04": iv_str_04,
            "ov_str_04_label": iv_str_04_label,
            "ov_str_05": iv_str_05,
            "ov_str_05_label": iv_str_05_label,
            "ov_str_06": iv_str_06,
            "ov_str_06_label": iv_str_06_label,
            
            "ov_int_01": iv_int_01,
            "ov_int_01_lable": iv_int_01_lable,
            "ov_int_02": iv_int_02,
            "ov_int_02_lable": iv_int_02_lable,
            "ov_int_03": iv_int_03,
            "ov_int_03_lable": iv_int_03_lable,

            "ov_double_01": iv_double_01,
            "ov_double_01_lable": iv_double_01_lable,
            "ov_double_02": iv_double_02,
            "ov_double_02_lable": iv_double_02_lable,

            "ov_bool_01": iv_bool_01,
            "ov_bool_01_label": iv_bool_01_label
        }
    }

    '''添加函数实现
    
    '''


    return json_ret 


if __name__ == '__main__':
    assets = {}
    params = {
        "iv_str_01": "iv_str_01",
        "iv_str_02": "iv_str_02",
        "iv_str_03": "iv_str_03",
        "iv_str_04": "iv_str_04",
        "iv_str_05": "iv_str_05",
        "iv_str_06": "iv_str_06",
        "iv_int_03": 3,
        "iv_int_02": 2,
        "iv_int_01": 1,
        "iv_bool_01": False
    }
    context_info = {}
    print(set_variable(params, assets, context_info))