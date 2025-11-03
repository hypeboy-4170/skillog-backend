#!/usr/bin/env python3
import json
import sys
import os
from fastapi.testclient import TestClient

# パスを追加
sys.path.append(os.path.dirname(__file__))

from main import app

client = TestClient(app)

def test_login_endpoint():
    """ログインエンドポイントのテスト"""
    print("=== ログインエンドポイントテスト ===")
    
    # 正常なリクエスト
    response = client.post("/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    
    print(f"ステータス: {response.status_code}")
    print(f"レスポンス: {response.json()}")
    
    # 不正なリクエスト
    response = client.post("/login", json={})
    print(f"不正リクエスト ステータス: {response.status_code}")

def test_register_endpoint():
    """ユーザー登録エンドポイントのテスト"""
    print("\n=== ユーザー登録エンドポイントテスト ===")
    
    response = client.post("/register", json={
        "username": "newuser",
        "password": "newpass123",
        "email": "test@example.com"
    })
    
    print(f"ステータス: {response.status_code}")
    print(f"レスポンス: {response.json()}")

def test_sendmail_endpoint():
    """メール送信エンドポイントのテスト"""
    print("\n=== メール送信エンドポイントテスト ===")
    
    # 認証なし
    response = client.post("/sendmail", json={
        "to": "test@example.com",
        "subject": "テスト",
        "body": "テストメール"
    })
    
    print(f"認証なし ステータス: {response.status_code}")
    print(f"レスポンス: {response.json()}")
    
    # 無効なトークン
    response = client.post("/sendmail", 
        json={
            "to": "test@example.com",
            "subject": "テスト",
            "body": "テストメール"
        },
        headers={"Authorization": "Bearer invalid-token"}
    )
    
    print(f"無効トークン ステータス: {response.status_code}")
    print(f"レスポンス: {response.json()}")

def test_cors():
    """CORS設定のテスト"""
    print("\n=== CORS設定テスト ===")
    
    response = client.options("/login")
    print(f"OPTIONS ステータス: {response.status_code}")
    print(f"CORS ヘッダー: {dict(response.headers)}")

if __name__ == "__main__":
    print("直接アクセステスト開始...")
    
    test_login_endpoint()
    test_register_endpoint() 
    test_sendmail_endpoint()
    test_cors()
    
    print("\nテスト完了")