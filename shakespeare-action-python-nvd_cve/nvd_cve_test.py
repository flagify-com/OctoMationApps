import unittest
from nvd_cve import health_check,cves


class TestYourCode(unittest.TestCase):
    def test_health_check(self):
        params = {}
        assets = {"proxy": "http://127.0.0.1:7890"}
        context_info = {}

        result = health_check(params, assets, context_info)
        self.assertEqual(result["code"], 200)

    def test_cves(self):
        params = {
            "keywordSearch": "chrome",
            "pubStartDate": "2023-01-01 00:00:00",
            "pubEndDate": "2023-01-31 23:59:59",
            "resultsPerPage": 10,
            "startIndex": 0
        }
        assets = {"proxy": "http://127.0.0.1:7890"}
        context_info = {}

        result = cves(params, assets, context_info)
        self.assertEqual(result["code"], 200)
        self.assertIn("records", result["data"])
        self.assertIn("resultsPerPage", result["data"])
        self.assertIn("startIndex", result["data"])
        self.assertIn("totalResults", result["data"])

if __name__ == '__main__':
    unittest.main()
