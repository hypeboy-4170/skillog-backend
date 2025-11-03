import json
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# パスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'login'))

from services.cognito import authenticate_user, verify_token
from login.login_handler import lambda_handler as login_handler

class TestCognitoAuth(unittest.TestCase):

    @patch('services.cognito.cognito_client')
    def test_authenticate_user_success(self, mock_client):
        # モック設定
        mock_client.admin_initiate_auth.return_value = {
            'AuthenticationResult': {
                'AccessToken': 'test-access-token'
            }
        }
        
        # テスト実行
        token = authenticate_user('testuser', 'testpass')
        
        # 検証
        self.assertEqual(token, 'test-access-token')
        mock_client.admin_initiate_auth.assert_called_once()

    @patch('services.cognito.cognito_client')
    def test_authenticate_user_failure(self, mock_client):
        # モック設定（認証失敗）
        from botocore.exceptions import ClientError
        mock_client.admin_initiate_auth.side_effect = ClientError(
            {'Error': {'Code': 'NotAuthorizedException'}}, 'AdminInitiateAuth'
        )
        
        # テスト実行と検証
        with self.assertRaises(Exception):
            authenticate_user('testuser', 'wrongpass')

    @patch('services.cognito.cognito_client')
    def test_verify_token_success(self, mock_client):
        # モック設定
        mock_client.get_user.return_value = {'Username': 'testuser'}
        
        # テスト実行
        result = verify_token('valid-token')
        
        # 検証
        self.assertTrue(result)

    @patch('services.cognito.cognito_client')
    def test_verify_token_failure(self, mock_client):
        # モック設定（トークン無効）
        from botocore.exceptions import ClientError
        mock_client.get_user.side_effect = ClientError(
            {'Error': {'Code': 'NotAuthorizedException'}}, 'GetUser'
        )
        
        # テスト実行
        result = verify_token('invalid-token')
        
        # 検証
        self.assertFalse(result)

    @patch('login.login_handler.authenticate_user')
    def test_login_handler_success(self, mock_auth):
        # モック設定
        mock_auth.return_value = 'test-access-token'
        
        # テストイベント
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'password': 'testpass'
            })
        }
        
        # テスト実行
        response = login_handler(event, {})
        
        # 検証
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertTrue(body['success'])
        self.assertEqual(body['access_token'], 'test-access-token')

    def test_login_handler_missing_credentials(self):
        # テストイベント（認証情報なし）
        event = {
            'body': json.dumps({})
        }
        
        # テスト実行
        response = login_handler(event, {})
        
        # 検証
        self.assertEqual(response['statusCode'], 400)
        body = json.loads(response['body'])
        self.assertIn('error', body)

    @patch('login.login_handler.authenticate_user')
    def test_login_handler_auth_failure(self, mock_auth):
        # モック設定（認証失敗）
        mock_auth.side_effect = Exception('Authentication failed')
        
        # テストイベント
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'password': 'wrongpass'
            })
        }
        
        # テスト実行
        response = login_handler(event, {})
        
        # 検証
        self.assertEqual(response['statusCode'], 401)
        body = json.loads(response['body'])
        self.assertIn('error', body)



if __name__ == '__main__':
    unittest.main()