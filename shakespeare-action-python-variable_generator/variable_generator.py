# -*- coding: utf-8 -*-


def set_variable(params, assets, context_info):
    """设置变量"""

    # 返回值
    json_ret = {
        "code": 200,
        "msg": "",
        "data": {
            "ov_str_01": "",
            "ov_str_01_label": "",
            "ov_str_02": "",
            "ov_str_02_label": "",
            "ov_str_03": "",
            "ov_str_03_label": "",
            "ov_str_04": "",
            "ov_str_04_label": "",
            "ov_str_05": "",
            "ov_str_05_label": "",
            "ov_str_06": "",
            "ov_str_06_label": "",
            
            "ov_int_01": 0,
            "ov_int_01_lable": "",
            "ov_int_02": 0,
            "ov_int_02_lable": "",
            "ov_int_03": 0,
            "ov_int_03_lable": "",

            "ov_long_01": 0,
            "ov_long_01_lable": "",
            "ov_long_02": 0,            
            "ov_long_02_lable": "",

            "ov_double_01": 0,
            "ov_double_01_lable": "",
            "ov_double_02": 0,
            "ov_double_02_lable": "",

            "ov_bool_01": False,
            "ov_bool_01_label": "",

            "ov_iv_jsonarray_01": [],
            "ov_iv_jsonarray_01_label": "",
            "ov_jsonobject_01": {},
            "ov_jsonobject_01_label": ""
        },
        "summary": {
            "statusCode": 0,
            "msg": ""
        }
    }

    iv_str_01 = params.get("iv_str_01", "")
    iv_str_01_label = params.get("iv_str_01_label", "")
    iv_str_02 = params.get("iv_str_02", "")
    iv_str_02_label = params.get("iv_str_02_label", "")
    iv_str_03 = params.get("iv_str_03", "")
    iv_str_03_label = params.get("iv_str_03_label", "")
    iv_str_04 = params.get("iv_str_04", "")
    iv_str_04_label = params.get("iv_str_04_label", "")
    iv_str_05 = params.get("iv_str_05", "")
    iv_str_05_label = params.get("iv_str_05_label", "")
    iv_str_06 = params.get("iv_str_06", "")
    iv_str_06_label = params.get("iv_str_06_label", "")

    iv_int_01 = params.get("iv_int_01", 0)
    iv_int_01_lable = params.get("iv_int_01_lable", "")
    iv_int_02 = params.get("iv_int_02", 0)
    iv_int_02_lable = params.get("iv_int_02_lable", "")
    iv_int_03 = params.get("iv_int_03", 0)
    iv_int_03_lable = params.get("iv_int_03_lable", "")

    iv_long_01 = params.get("iv_long_01", 0)
    iv_long_01_lable = params.get("iv_long_01_lable", "")
    iv_long_02 = params.get("iv_long_02", 0)
    iv_long_02_lable = params.get("iv_long_02_lable", "")

    iv_double_01 = params.get("iv_double_01", 0.0)
    iv_double_01_lable = params.get("iv_double_01_lable", "")
    iv_double_02 = params.get("iv_double_02", 0.0)
    iv_double_02_lable = params.get("iv_double_02_lable", "")

    iv_bool_01 = params.get("iv_bool_01", False)
    iv_bool_01_label = params.get("iv_bool_01_label", "")

    iv_jsonarray_01 = params.get("iv_jsonarray_01", [])
    iv_jsonarray_01_label = params.get("iv_jsonarray_01_label", "")
    iv_jsonobject_01 = params.get("iv_jsonobject_01", {})
    iv_jsonobject_01_label = params.get("iv_jsonobject_01_label", "")

    try:
        json_ret["data"]["ov_str_01"] = iv_str_01
        json_ret["data"]["ov_str_01_label"] = iv_str_01_label
        json_ret["data"]["ov_str_02"] = iv_str_02
        json_ret["data"]["ov_str_02_label"] = iv_str_02_label
        json_ret["data"]["ov_str_03"] = iv_str_03
        json_ret["data"]["ov_str_03_label"] = iv_str_03_label
        json_ret["data"]["ov_str_04"] = iv_str_04
        json_ret["data"]["ov_str_04_label"] = iv_str_04_label
        json_ret["data"]["ov_str_05"] = iv_str_05
        json_ret["data"]["ov_str_05_label"] = iv_str_05_label
        json_ret["data"]["ov_str_06"] = iv_str_06
        json_ret["data"]["ov_str_06_label"] = iv_str_06_label
        
        json_ret["data"]["ov_int_01"] = int(iv_int_01)
        json_ret["data"]["ov_int_01_lable"] = iv_int_01_lable
        json_ret["data"]["ov_int_02"] = int(iv_int_02)
        json_ret["data"]["ov_int_02_lable"] = iv_int_02_lable
        json_ret["data"]["ov_int_03"] = int(iv_int_03)
        json_ret["data"]["ov_int_03_lable"] = iv_int_03_lable

        json_ret["data"]["ov_long_01"] = int(iv_long_01)
        json_ret["data"]["ov_long_01_lable"] = iv_long_01_lable
        json_ret["data"]["ov_long_02"] = int(iv_long_02)
        json_ret["data"]["ov_long_02_lable"] = iv_long_02_lable


        json_ret["data"]["ov_double_01"] = float(iv_double_01)
        json_ret["data"]["ov_double_01_lable"] = iv_double_01_lable
        json_ret["data"]["ov_double_02"] = float(iv_double_02)
        json_ret["data"]["ov_double_02_lable"] = iv_double_02_lable

        json_ret["data"]["ov_bool_01"] = bool(iv_bool_01)
        json_ret["data"]["ov_bool_01_label"] = iv_bool_01_label

        json_ret["data"]["ov_iv_jsonarray_01"] = iv_jsonarray_01
        json_ret["data"]["ov_iv_jsonarray_01_label"] = iv_jsonarray_01_label
        json_ret["data"]["ov_jsonobject_01"] = iv_jsonobject_01
        json_ret["data"]["ov_jsonobject_01_label"] = iv_jsonobject_01_label
    except Exception as e:
        json_ret["summary"]["statusCode"] = 500
        json_ret["summary"]["msg"] = f"设置变量失败:{e}"
    

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
        "iv_int_03": -1,
        "iv_int_02": 2,
        "iv_int_01": 1,
        "iv_long_01": "",
        "iv_long_02": 1000,
        "iv_bool_01": False,
        "iv_jsonarray_01": [{"a":1,"b":2}, {"c":3,"d":4}],
        "iv_jsonobject_01": {"name": "iv_jsonobject_01", "age": 18}
    }
    context_info = {}
    print(set_variable(params, assets, context_info))