#!/usr/bin/env python3
import os
import sys

# テスト用にCLIENT_SECRETを設定（実際の値は別途設定が必要）
os.environ['CLIENT_SECRET'] = 'test-secret'

sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from services.cognito import authenticate_user

def test_with_secret():
    """SECRET_HASH対応後のテスト"""
    username = "testuser7"
    password = "TestPass123!"
    
    print(f"=== SECRET_HASH対応テスト ===")
    print(f"CLIENT_SECRET設定: {'あり' if os.environ.get('CLIENT_SECRET') else 'なし'}")
    
    try:
        token = authenticate_user(username, password)
        print(f"ログイン成功")
        print(f"トークン: {token[:50]}...")
        return True
        
    except Exception as e:
        print(f"ログイン失敗: {e}")
        return False

if __name__ == "__main__":
    test_with_secret()