#!/usr/bin/env python3
import requests
import boto3

def check_s3_bucket_policy():
    """S3バケットポリシーを確認"""
    print("=== S3バケットポリシー確認 ===")
    
    bucket_name = "skilog-website-764520352108-ap-northeast-1"
    
    try:
        s3 = boto3.client('s3', region_name='ap-northeast-1')
        
        # バケットポリシーを取得
        try:
            policy = s3.get_bucket_policy(Bucket=bucket_name)
            print("バケットポリシーが設定されています")
            print(policy['Policy'][:200] + "...")
        except s3.exceptions.NoSuchBucketPolicy:
            print("バケットポリシーが設定されていません")
            
        # CORS設定を確認
        try:
            cors = s3.get_bucket_cors(Bucket=bucket_name)
            print("CORS設定:")
            for rule in cors['CORSRules']:
                print(f"  Methods: {rule['AllowedMethods']}")
                print(f"  Origins: {rule['AllowedOrigins']}")
        except:
            print("CORS設定なし")
            
    except Exception as e:
        print(f"S3確認エラー: {e}")

def test_direct_s3():
    """S3に直接アクセステスト"""
    print("\n=== S3直接アクセステスト ===")
    
    s3_url = "https://skilog-website-764520352108-ap-northeast-1.s3-website-ap-northeast-1.amazonaws.com"
    
    try:
        response = requests.get(f"{s3_url}/api/login", timeout=5)
        print(f"S3直接アクセス: {response.status_code}")
        print(f"Response: {response.text[:100]}")
    except Exception as e:
        print(f"S3アクセスエラー: {e}")

def check_cloudfront_logs():
    """CloudFrontのレスポンスヘッダーを詳細確認"""
    print("\n=== CloudFrontレスポンスヘッダー詳細 ===")
    
    try:
        response = requests.post("https://allforone-freesite.com/api/login", 
                               json={"test": "data"}, timeout=5)
        
        print(f"Status: {response.status_code}")
        print("重要なヘッダー:")
        
        important_headers = [
            'server', 'x-amz-cf-id', 'x-amz-cf-pop', 'x-cache',
            'x-amz-apigw-id', 'x-amzn-requestid', 'via'
        ]
        
        for header in important_headers:
            if header in response.headers:
                print(f"  {header}: {response.headers[header]}")
                
        # エラーコードを確認
        if "AccessDenied" in response.text:
            print("  → S3 AccessDenied エラー")
        elif "SignatureDoesNotMatch" in response.text:
            print("  → 署名エラー")
            
    except Exception as e:
        print(f"ヘッダー確認エラー: {e}")

if __name__ == "__main__":
    print("403エラー詳細診断...")
    
    check_s3_bucket_policy()
    test_direct_s3()
    check_cloudfront_logs()
    
    print("\n診断完了")