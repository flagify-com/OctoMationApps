import unittest
from ssh_req import ssh_execute

class TestSSHFunc(unittest.TestCase):
	def test_ssh_execute(self):
		params = {
			"cmd": "ls",
			"ret_flag": "%"
		} 
		assets = {}
		context_info = {}
		print(ssh_execute(params, assets, context_info))


if __name__ == "__main__":
	suite = unittest.TestSuite()
	suite.addTest(TestSSHFunc('test_ssh_execute'))
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)
