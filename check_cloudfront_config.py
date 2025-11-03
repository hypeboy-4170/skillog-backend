#!/usr/bin/env python3
import boto3
import json

def check_cloudfront_distribution():
    """CloudFront設定を確認"""
    print("=== CloudFront設定確認 ===")
    
    distribution_id = "E34ZMEPX9776JV"
    
    try:
        client = boto3.client('cloudfront', region_name='us-east-1')
        
        # Distribution設定を取得
        response = client.get_distribution(Id=distribution_id)
        config = response['Distribution']['DistributionConfig']
        
        print(f"Distribution ID: {distribution_id}")
        print(f"Status: {response['Distribution']['Status']}")
        print(f"Domain: {config['Aliases']['Items'][0] if config['Aliases']['Quantity'] > 0 else 'None'}")
        
        # Origins確認
        print("\nOrigins:")
        for i, origin in enumerate(config['Origins']['Items']):
            print(f"  {i+1}. {origin['Id']}")
            print(f"     Domain: {origin['DomainName']}")
            print(f"     Path: {origin.get('OriginPath', '/')}")
        
        # Behaviors確認
        print("\nBehaviors:")
        print(f"  Default: -> {config['DefaultCacheBehavior']['TargetOriginId']}")
        
        if config['CacheBehaviors']['Quantity'] > 0:
            for behavior in config['CacheBehaviors']['Items']:
                print(f"  {behavior['PathPattern']} -> {behavior['TargetOriginId']}")
        
        return config
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def suggest_fix():
    """修正案を提示"""
    print("\n=== 修正案 ===")
    print("1. CloudFrontのOriginがS3を指している可能性があります")
    print("2. /api/* パスをAPI Gatewayにルーティングする設定が必要です")
    print("3. 以下のコマンドで修正できます:")
    print("   bash update-cloudfront.sh")

if __name__ == "__main__":
    config = check_cloudfront_distribution()
    suggest_fix()