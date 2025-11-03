#!/usr/bin/env python3
import requests
import json

CLOUDFRONT_URL = "https://allforone-freesite.com"
API_GATEWAY_URL = "https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod"

def test_path_variations():
    """パスのバリエーションをテスト"""
    print("=== パスバリエーションテスト ===")
    
    paths = [
        "/api/login",
        "/api",
        "/login", 
        "/prod/login",
        ""
    ]
    
    for path in paths:
        url = f"{CLOUDFRONT_URL}{path}"
        try:
            response = requests.get(url, timeout=5)
            print(f"{path:15} -> {response.status_code}")
            if response.status_code != 403:
                print(f"                Response: {response.text[:100]}")
        except Exception as e:
            print(f"{path:15} -> Error: {e}")

def test_headers():
    """ヘッダー情報を詳細確認"""
    print("\n=== ヘッダー詳細確認 ===")
    
    urls = [
        ("CloudFront", f"{CLOUDFRONT_URL}/api/login"),
        ("Direct API", f"{API_GATEWAY_URL}/login")
    ]
    
    for name, url in urls:
        print(f"\n{name}:")
        try:
            response = requests.post(url, json={"test": "data"}, timeout=5)
            print(f"  Status: {response.status_code}")
            
            important_headers = [
                'server', 'x-amz-cf-id', 'x-amzn-requestid', 
                'content-type', 'access-control-allow-origin'
            ]
            
            for header in important_headers:
                if header in response.headers:
                    print(f"  {header}: {response.headers[header]}")
                    
        except Exception as e:
            print(f"  Error: {e}")

def test_methods():
    """HTTPメソッドのテスト"""
    print("\n=== HTTPメソッドテスト ===")
    
    methods = ["GET", "POST", "OPTIONS", "PUT", "DELETE"]
    
    for method in methods:
        try:
            response = requests.request(method, f"{CLOUDFRONT_URL}/api", timeout=5)
            print(f"{method:8} -> {response.status_code}")
        except Exception as e:
            print(f"{method:8} -> Error: {e}")

if __name__ == "__main__":
    print("CloudFront 診断開始...")
    
    test_path_variations()
    test_headers()
    test_methods()
    
    print("\n診断完了")