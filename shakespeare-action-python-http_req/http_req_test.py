import unittest
from http_req import http_requests

class TestHTTPFunc(unittest.TestCase):
	def test_requests(self):
		params = {
			"headers": "{'Content-Type': 'application/json', 'User-Agent': 'HG-APP'}",
			"method": "GET",
			"ssl_verify": False,
			"url": "https://api.uomg.com/api/rand.qinghua?format=json"
		} 
		assets = {}
		context_info = {}
		print(http_requests(params, assets, context_info))


if __name__ == "__main__":
	suite = unittest.TestSuite()
	suite.addTest(TestHTTPFunc('test_requests'))
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)
