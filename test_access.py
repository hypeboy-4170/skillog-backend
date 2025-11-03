#!/usr/bin/env python3
import requests
import json
import sys

# API_BASE_URL = "https://your-api-gateway-url.execute-api.ap-northeast-1.amazonaws.com/prod"
API_BASE_URL = "http://localhost:8000"  # ローカルテスト用

def test_login():
    """ログインエンドポイントのテスト"""
    print("=== ログインテスト ===")
    
    # テストデータ
    login_data = {
        "username": "testuser",
        "password": "testpass"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/login", json=login_data)
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.json()}")
        
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
        
    except Exception as e:
        print(f"エラー: {e}")
        return None

def test_register():
    """ユーザー登録エンドポイントのテスト"""
    print("\n=== ユーザー登録テスト ===")
    
    register_data = {
        "username": "newuser",
        "password": "newpass123",
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/register", json=register_data)
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.json()}")
        
    except Exception as e:
        print(f"エラー: {e}")

def test_sendmail(token):
    """メール送信エンドポイントのテスト"""
    print("\n=== メール送信テスト ===")
    
    if not token:
        print("トークンがないためスキップ")
        return
    
    email_data = {
        "to": "recipient@example.com",
        "subject": "テストメール",
        "body": "これはテストメールです。"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/sendmail", json=email_data, headers=headers)
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.json()}")
        
    except Exception as e:
        print(f"エラー: {e}")

def test_unauthorized_access():
    """認証なしアクセスのテスト"""
    print("\n=== 認証なしアクセステスト ===")
    
    email_data = {
        "to": "test@example.com",
        "subject": "テスト",
        "body": "テスト"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/sendmail", json=email_data)
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.json()}")
        
    except Exception as e:
        print(f"エラー: {e}")

def run_all_tests():
    """全テストを実行"""
    print("API アクセステスト開始...")
    
    # 1. ログインテスト
    token = test_login()
    
    # 2. ユーザー登録テスト
    test_register()
    
    # 3. メール送信テスト（認証あり）
    test_sendmail(token)
    
    # 4. 認証なしアクセステスト
    test_unauthorized_access()
    
    print("\nテスト完了")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        global API_BASE_URL
        API_BASE_URL = sys.argv[1]
        print(f"API URL: {API_BASE_URL}")
    
    run_all_tests()