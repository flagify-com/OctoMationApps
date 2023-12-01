import unittest
import os
from http_client import http_request

class TestStringMethods(unittest.TestCase):
    params1 = {
            "SERVER": "https://www.baidu.com",
            "PATH": "/",
            "VERIFY_SSL": True,
            "COOKIE_FILE":"__RANDOM__COOKIE__FILE__"
    }
    params2 = {
            "SERVER": "https://www.baidu.com/",
            "PATH": "/s",
            "QUERY": "wd=chatgpt",
            "VERIFY_SSL": True,
            "COOKIE_FILE": ""
    }
    def test_http_200(self):
        params = {
            "SERVER": "https://www.baidu.com",
            "PATH": "/",
            "VERIFY_SSL": True,
            "COOKIE_FILE":"__RANDOM__COOKIE__FILE__"
        }
        req = http_request(params, None, None)
        self.assertEqual(req['data']['http_response_code'], 200)

    def test_http_404(self):
        params = {
            "SERVER": "https://www.baidu.com",
            "PATH": "/",
            "VERIFY_SSL": True,
            "COOKIE_FILE":"__RANDOM__COOKIE__FILE__"
        }
        params['PATH'] = '/4044444'
        req = http_request(params, None, None)
        self.assertEqual(req['data']['http_response_code'], 404)

    def test_exception_500(self):
        params = {
            "SERVER": "https://www.baidu.com",
            "PATH": "/",
            "VERIFY_SSL": True,
            "COOKIE_FILE":"__RANDOM__COOKIE__FILE__"
        }
        params['SERVER'] = 'http://127.0.0.1:65531'
        req = http_request(params, None, None)
        self.assertEqual(req['code'], 500)

    def test_cookie_1(self):
        params = {
            "SERVER": "https://www.baidu.com",
            "PATH": "/",
            "VERIFY_SSL": True,
            "COOKIE_FILE":"__RANDOM__COOKIE__FILE__"
        }
        req = http_request(params, None, None)
        self.assertTrue(os.path.exists(req['data']['cookie_file']), True)

    def test_cookie_2(self):
        params1 = {
                "SERVER": "https://www.baidu.com",
                "PATH": "/",
                "VERIFY_SSL": True,
                "COOKIE_FILE":"__RANDOM__COOKIE__FILE__"
        }
        params2 = {
                "SERVER": "https://www.baidu.com/",
                "PATH": "/s",
                "QUERY": "wd=chatgpt",
                "VERIFY_SSL": True,
                "COOKIE_FILE": ""
        }
        req = http_request(params1, None, None)
        params2['COOKIE_FILE'] = req['data']['cookie_file']
        req = http_request(params1, None, None)
        self.assertRegex(req['data']['cookies'], r'\S+=\S+')
    

    def test_cookie_3(self):
        params1 = {
            "SERVER": "https://www.baidu.com",
            "PATH": "/",
            "VERIFY_SSL": True,
            "COOKIE_FILE":"__RANDOM__COOKIE__FILE__"
        }
        params1['SERVER'] = 'http://setcookie.net'
        params1['COOKIES'] = "COOKIE_TEST_01=COOKIE_TEST_01_VALUE; COOKIE_TEST_02=COOKIE_TEST_02_VALUE"
        req = http_request(params1, None, None)
        self.assertRegex(req['data']['http_response_text'], r'COOKIE_TEST_01_VALUE')

    def test_header(self):
        params = {
            "SERVER": "https://www.baidu.com",
            "PATH": "/",
            "VERIFY_SSL": True,
            "COOKIE_FILE":""
        }
        req = http_request(params, None, None)
        self.assertEqual(req['data']['http_response_headers']['Content-Type'], 'text/html')

if __name__ == '__main__':
    unittest.main()