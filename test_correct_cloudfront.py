#!/usr/bin/env python3
import requests
import json
import time

# 正しいCloudFrontパス
CLOUDFRONT_BASE = "https://allforone-freesite.com/api"
API_GATEWAY_BASE = "https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod"

def test_endpoints():
    """正しいパスでエンドポイントをテスト"""
    print("=== 正しいパスでのエンドポイントテスト ===")
    
    test_cases = [
        {
            "name": "ログイン",
            "endpoint": "/login",
            "method": "POST",
            "data": {"username": "testuser", "password": "TestPass123"}
        },
        {
            "name": "ユーザー登録", 
            "endpoint": "/register",
            "method": "POST",
            "data": {"username": "newuser", "password": "NewPass123", "email": "test@example.com"}
        },
        {
            "name": "メール送信（認証なし）",
            "endpoint": "/sendmail",
            "method": "POST", 
            "data": {"to": "test@example.com", "subject": "test", "body": "test"}
        }
    ]
    
    for case in test_cases:
        print(f"\n--- {case['name']} ---")
        
        # CloudFront経由
        cf_url = f"{CLOUDFRONT_BASE}{case['endpoint']}"
        try:
            if case['method'] == 'POST':
                cf_response = requests.post(cf_url, json=case['data'], timeout=10)
            else:
                cf_response = requests.get(cf_url, timeout=10)
            
            print(f"CloudFront: {cf_response.status_code}")
            if cf_response.text:
                try:
                    cf_json = cf_response.json()
                    print(f"  Response: {cf_json}")
                except:
                    print(f"  Response: {cf_response.text[:100]}")
        except Exception as e:
            print(f"CloudFront: Error - {e}")
        
        # 直接API Gateway
        api_url = f"{API_GATEWAY_BASE}{case['endpoint']}"
        try:
            if case['method'] == 'POST':
                api_response = requests.post(api_url, json=case['data'], timeout=10)
            else:
                api_response = requests.get(api_url, timeout=10)
            
            print(f"Direct API: {api_response.status_code}")
            if api_response.text:
                try:
                    api_json = api_response.json()
                    print(f"  Response: {api_json}")
                except:
                    print(f"  Response: {api_response.text[:100]}")
        except Exception as e:
            print(f"Direct API: Error - {e}")

def test_cors():
    """CORS設定をテスト"""
    print("\n=== CORS設定テスト ===")
    
    headers = {
        "Origin": "https://allforone-freesite.com",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type,Authorization"
    }
    
    try:
        response = requests.options(f"{CLOUDFRONT_BASE}/login", headers=headers, timeout=10)
        print(f"OPTIONS /login: {response.status_code}")
        
        cors_headers = {k: v for k, v in response.headers.items() 
                       if k.lower().startswith("access-control")}
        for k, v in cors_headers.items():
            print(f"  {k}: {v}")
            
    except Exception as e:
        print(f"CORS test error: {e}")

def test_performance():
    """パフォーマンス比較"""
    print("\n=== パフォーマンス比較 ===")
    
    test_data = {"username": "test", "password": "Test123"}
    
    # CloudFront
    start = time.time()
    try:
        requests.post(f"{CLOUDFRONT_BASE}/login", json=test_data, timeout=10)
        cf_time = time.time() - start
        print(f"CloudFront: {cf_time:.3f}秒")
    except:
        print("CloudFront: エラー")
    
    # Direct API
    start = time.time()
    try:
        requests.post(f"{API_GATEWAY_BASE}/login", json=test_data, timeout=10)
        api_time = time.time() - start
        print(f"Direct API: {api_time:.3f}秒")
    except:
        print("Direct API: エラー")

if __name__ == "__main__":
    print("CloudFront 正しいパステスト開始...")
    
    test_endpoints()
    test_cors()
    test_performance()
    
    print("\nテスト完了")