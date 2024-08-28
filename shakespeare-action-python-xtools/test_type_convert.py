import unittest
from om_python_xtools import type_to_type

class TestTypeConvert(unittest.TestCase):
    def test_int_to_str(self):
        params = {
            "input_value": "3",
            "type_to": "string"
        }
        assets = {}
        context_info = {}
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertEqual(result["data"]["converted_value_string"], "3")

    def test_int_to_long(self):
        params = {
            "input_value": "-3",
            "type_to": "long"
        }
        assets = {}
        context_info = {}
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertEqual(result["data"]["converted_value_long"], -3)
        params = {
            "input_value": "abc",
            "type_to": "long"
        }
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 400)
        self.assertEqual(result["data"]["converted_value_long"], 0)

    def test_float_to_int(self):
        params = {
            "input_value": "3.14",
            "type_to": "integer"
        }
        assets = {}
        context_info = {}
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertEqual(result["data"]["converted_value_integer"], 3)
        params = {
            "input_value": "abc",
            "type_to": "integer"
        }
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 400)

    def test_str_to_bool(self):
        params = {
            "input_value": "true",
            "type_to": "boolean"
        }
        assets = {}
        context_info = {}
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertEqual(result["data"]["converted_value_boolean"], True)
        params = {
            "input_value": "No",
            "type_to": "boolean"
        }
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertEqual(result["data"]["converted_value_boolean"], False)
        params = {
            "input_value": "abc",
            "type_to": "boolean"
        }
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 400)

    def test_str_to_jsonarry(self):
        params = {
            "input_value": '[{"name": "apple"}, {"name": "banana"}, {"name": "cherry"}]',
            "type_to": "jsonarray"
        }
        assets = {}
        context_info = {}
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertEqual(result["data"]["converted_value_jsonarray"][0]["name"], "apple")
        params = {
            "input_value": "abc",
            "type_to": "jsonarray"
        }
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 400)

    def test_string_to_jsonobject(self):
        params = {
            "input_value": '{"name": "apple", "price": 1.99, "result": false}',
            "type_to": "jsonobject" 
        }
        assets = {}
        context_info = {}
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 0)
        self.assertEqual(result["data"]["converted_value_jsonobject"]["result"], False)
        params = {
            "input_value": "abc",
            "type_to": "jsonobject"
        }
        result = type_to_type(params, assets, context_info)
        self.assertEqual(result["summary"]["statusCode"], 400)

if __name__ == '__main__':
    unittest.main()