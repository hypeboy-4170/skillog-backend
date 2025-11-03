#!/usr/bin/env python3
import requests

def test_simple():
    """シンプルなテスト"""
    print("=== シンプルテスト ===")
    
    # CloudFront経由
    try:
        response = requests.get("https://allforone-freesite.com/api", timeout=10)
        print(f"CloudFront /api: {response.status_code}")
        print(f"Server: {response.headers.get('server', 'Unknown')}")
        
        if response.status_code == 403:
            print("まだS3にルーティングされています")
        elif response.status_code == 404:
            print("API Gatewayにルーティングされています（正常）")
            
    except Exception as e:
        print(f"エラー: {e}")
    
    # 直接API Gateway
    try:
        response = requests.get("https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod", timeout=10)
        print(f"Direct API: {response.status_code}")
    except Exception as e:
        print(f"Direct APIエラー: {e}")

if __name__ == "__main__":
    test_simple()