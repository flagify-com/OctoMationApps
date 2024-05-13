import unittest
from gemini import generateContent

class TestGenerateContent(unittest.TestCase):
    def test_generate_content_happy_path(self):
        params = {"question": "Hi"}
        assets = {
            "key": "RIGHT_KEY",
            "api_host": "generativelanguage.googleapis.com"
        }
        context_info = {}

        result = generateContent(params, assets, context_info)

        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"]["err_code"], 200)

    def test_generate_content_api_failure(self):
        params = {"question": "Hi"}
        assets = {
            "key": "ERROR_KEY",
            "api_host": "generativelanguage.googleapis.com"
        }
        context_info = {}

        result = generateContent(params, assets, context_info)

        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"]["err_code"], 400)
        


if __name__ == '__main__':
    unittest.main()