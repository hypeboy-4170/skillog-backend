#!/usr/bin/env python3
import requests
import json
import time

# CloudFront URL
CLOUDFRONT_URL = "https://allforone-freesite.com/api"
API_GATEWAY_URL = "https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod"

def test_endpoint(base_url, endpoint, method="GET", data=None, headers=None):
    """エンドポイントをテスト"""
    url = f"{base_url}{endpoint}"
    
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "OPTIONS":
            response = requests.options(url, headers=headers, timeout=10)
        else:
            response = requests.get(url, headers=headers, timeout=10)
        
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text[:200] if response.text else None
        }
    except Exception as e:
        return {"error": str(e)}

def test_cloudfront_vs_direct():
    """CloudFront vs 直接API Gateway比較テスト"""
    print("=== CloudFront vs API Gateway 比較テスト ===")
    
    test_cases = [
        {"endpoint": "/login", "method": "POST", "data": {"username": "test", "password": "test"}},
        {"endpoint": "/register", "method": "POST", "data": {"username": "test", "password": "Test123", "email": "test@example.com"}},
        {"endpoint": "/", "method": "OPTIONS"}
    ]
    
    for case in test_cases:
        print(f"\n--- {case['method']} {case['endpoint']} ---")
        
        # CloudFront経由
        print("CloudFront:")
        cf_result = test_endpoint(CLOUDFRONT_URL, case["endpoint"], 
                                case["method"], case.get("data"))
        print(f"  Status: {cf_result.get('status_code', 'ERROR')}")
        if "error" in cf_result:
            print(f"  Error: {cf_result['error']}")
        
        # 直接API Gateway
        print("Direct API:")
        direct_result = test_endpoint(API_GATEWAY_URL, case["endpoint"], 
                                    case["method"], case.get("data"))
        print(f"  Status: {direct_result.get('status_code', 'ERROR')}")
        if "error" in direct_result:
            print(f"  Error: {direct_result['error']}")

def test_cors_headers():
    """CORS ヘッダーのテスト"""
    print("\n=== CORS ヘッダーテスト ===")
    
    headers = {
        "Origin": "https://allforone-freesite.com",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type,Authorization"
    }
    
    print("CloudFront CORS:")
    cf_result = test_endpoint(CLOUDFRONT_URL, "/login", "OPTIONS", headers=headers)
    if "error" not in cf_result:
        cors_headers = {k: v for k, v in cf_result["headers"].items() 
                       if k.lower().startswith("access-control")}
        for k, v in cors_headers.items():
            print(f"  {k}: {v}")
    else:
        print(f"  Error: {cf_result['error']}")

def test_authentication_flow():
    """認証フローのテスト"""
    print("\n=== 認証フローテスト ===")
    
    # 1. ログイン試行
    login_data = {"username": "testuser", "password": "TestPass123"}
    
    print("1. ログイン試行 (CloudFront):")
    login_result = test_endpoint(CLOUDFRONT_URL, "/login", "POST", login_data)
    print(f"   Status: {login_result.get('status_code')}")
    
    # 2. 認証が必要なエンドポイントへのアクセス
    print("2. 認証なしでメール送信試行:")
    mail_data = {"to": "test@example.com", "subject": "test", "body": "test"}
    mail_result = test_endpoint(CLOUDFRONT_URL, "/sendmail", "POST", mail_data)
    print(f"   Status: {mail_result.get('status_code')}")

def test_performance():
    """パフォーマンステスト"""
    print("\n=== パフォーマンステスト ===")
    
    endpoints = ["/login", "/register"]
    
    for endpoint in endpoints:
        print(f"\n{endpoint} レスポンス時間:")
        
        # CloudFront
        start_time = time.time()
        cf_result = test_endpoint(CLOUDFRONT_URL, endpoint, "POST", 
                                {"username": "test", "password": "Test123"})
        cf_time = time.time() - start_time
        print(f"  CloudFront: {cf_time:.3f}秒")
        
        # 直接API
        start_time = time.time()
        direct_result = test_endpoint(API_GATEWAY_URL, endpoint, "POST", 
                                    {"username": "test", "password": "Test123"})
        direct_time = time.time() - start_time
        print(f"  Direct API: {direct_time:.3f}秒")

if __name__ == "__main__":
    print("CloudFront アクセステスト開始...")
    
    test_cloudfront_vs_direct()
    test_cors_headers()
    test_authentication_flow()
    test_performance()
    
    print("\nテスト完了")