#!/usr/bin/env python3
"""
Cognito認証のマニュアルテスト用スクリプト
実際のAWS Cognitoサービスに対してテストを実行
"""
import json
import sys
import os

# パスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'login'))

from services.cognito import authenticate_user, verify_token
from login.login_handler import lambda_handler as login_handler

def test_login_handler():
    """ログインハンドラーのテスト"""
    print("=== ログインハンドラーテスト ===")
    
    # テストケース1: 正常なリクエスト（実際の認証は失敗する可能性あり）
    event = {
        'body': json.dumps({
            'username': 'testuser',
            'password': 'testpass'
        })
    }
    
    try:
        response = login_handler(event, {})
        print(f"ステータスコード: {response['statusCode']}")
        print(f"レスポンス: {response['body']}")
    except Exception as e:
        print(f"エラー: {e}")
    
    # テストケース2: 不正なリクエスト
    event_invalid = {
        'body': json.dumps({})
    }
    
    response = login_handler(event_invalid, {})
    print(f"\n不正リクエストのステータスコード: {response['statusCode']}")
    print(f"レスポンス: {response['body']}")

def test_cognito_functions():
    """Cognito関数の直接テスト"""
    print("\n=== Cognito関数直接テスト ===")
    
    try:
        # 認証テスト（実際のユーザーが存在しない場合は失敗）
        token = authenticate_user('testuser', 'testpass')
        print(f"認証成功: {token[:20]}...")
        
        # トークン検証テスト
        is_valid = verify_token(token)
        print(f"トークン検証: {is_valid}")
        
    except Exception as e:
        print(f"認証エラー（予想される）: {e}")

if __name__ == "__main__":
    test_login_handler()
    test_cognito_functions()
    print("\n✅ マニュアルテスト完了")