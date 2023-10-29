import unittest
from unittest.mock import patch
from redhat_cve_search import get_cve, get_cve_details

class TestYourFunctions(unittest.TestCase):

    @patch('redhat_cve_search.requests.get')
    def test_get_cve(self, mock_get):
        mock_response = {
            "data": [{"CVE": "CVE-1234", "severity": "low", "public_date": "2022-01-01", "advisories": "adv", "bugzilla": "bz", "bugzilla_description": "desc", "cvss_score": "5.6", "cvss_scoring_vector": "vector", "CWE": "CWE-123", "affected_packages": "package", "resource_url": "url", "cvss3_scoring_vector": "vector", "cvss3_score": "6.7"}],
            "code": 200,
            "msg": ""
        }
        mock_get.return_value.json.return_value = mock_response
        assets = {"proxy": "your_proxy"}
        params = {"before": "2023-01-01", "per_page": 5}
        result = get_cve(params, assets, context_info=None)
        self.assertEqual(result["code"], 200)

    @patch('redhat_cve_search.requests.get')
    def test_get_cve_details(self, mock_get):
        mock_response = {
            "data": {"threat_severity": "low", "public_date": "2022-01-01", "bugzilla": "bz", "cvss3": "cvss3", "cwe": "CWE-123", "details": "details", "affected_release": "release", "package_state": "state", "upstream_fix": "fix", "references": "ref", "name": "name", "csaw": "csaw"},
            "code": 200,
            "msg": ""
        }
        mock_get.return_value.json.return_value = mock_response
        assets = {"proxy": "your_proxy"}
        params = {"id": "CVE-1234"}
        result = get_cve_details(params, assets, context_info=None)
        self.assertEqual(result["code"], 200)

if __name__ == '__main__':
    unittest.main()
