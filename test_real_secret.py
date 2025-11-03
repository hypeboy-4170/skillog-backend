#!/usr/bin/env python3
import os
import sys

# 実際のCLIENT_SECRETを設定
os.environ['CLIENT_SECRET'] = '1cf7q4beajh4jjcqm04os3hkqbe7mbp6gdv46qrgd3esegrkj1hi'

sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from services.cognito import authenticate_user

def test_real_secret():
    """実際のCLIENT_SECRETでテスト"""
    username = "testuser7"
    password = "TestPass123!"
    
    print(f"=== 実際のSECRET_HASHテスト ===")
    
    try:
        token = authenticate_user(username, password)
        print(f"✅ ログイン成功")
        print(f"トークン: {token[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ ログイン失敗: {e}")
        return False

if __name__ == "__main__":
    test_real_secret()