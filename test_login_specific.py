#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from services.cognito import authenticate_user

def test_specific_login():
    """特定ユーザーでのログインテスト"""
    username = "testuser7"
    password = "TestPass123!"
    
    print(f"=== {username} ログインテスト ===")
    
    try:
        token = authenticate_user(username, password)
        print(f"✅ ログイン成功")
        print(f"トークン: {token[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ ログイン失敗: {e}")
        return False

if __name__ == "__main__":
    test_specific_login()