import unittest
from unittest.mock import patch
from awvs import add_targets  # 假设awvs是文件名，并且已经正确地import了add_targets函数

class TestAddTargets(unittest.TestCase):
    def setUp(self):
        self.params = {
            'address': '127.0.0.1',
            'description': 'Test Target',
            'criticality': 5
        }
        self.assets = {
            'token': 'dummy_token',
            'awvs_address': 'https://localhost:3443/'
        }
        self.context_info = {}  # 根据实际情况填充

    @patch('awvs.requests.post')
    def test_add_targets_success(self, mock_post):
        # 模拟成功的HTTP响应
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'address': self.params['address'],
            'description': self.params['description'],
            'domain': 'localhost',
            'target_id': '1'
        }

        result = add_targets(self.params, self.assets, self.context_info)
        self.assertEqual(result['code'], 200)
        self.assertEqual(result['msg'], '')
        self.assertEqual(result['data'], {
            'address': self.params['address'],
            'description': self.params['description'],
            'domain': 'localhost',
            'target_id': '1'
        })

    @patch('awvs.requests.post')
    def test_add_targets_http_error(self, mock_post):
        # 模拟HTTP错误
        mock_response = mock_post.return_value
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'Bad Request'}

        result = add_targets(self.params, self.assets, self.context_info)
        self.assertEqual(result['code'], 200)
        self.assertNotEqual(result['msg'], 'Connection error')
        self.assertEqual(result['data'], {'address': '', 'description': '', 'domain': '', 'target_id': ''})

    @patch('awvs.requests.post')
    def test_add_targets_connection_error(self, mock_post):
        # 模拟连接错误
        mock_post.side_effect = Exception('Connection error')

        result = add_targets(self.params, self.assets, self.context_info)
        self.assertEqual(result['code'], 200)
        self.assertNotEqual(result['msg'], '')
        self.assertEqual(result['data'], {'address': '', 'description': '', 'domain': '', 'target_id': ''})

if __name__ == '__main__':
    unittest.main()