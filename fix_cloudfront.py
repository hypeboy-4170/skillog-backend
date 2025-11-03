#!/usr/bin/env python3
import boto3
import json

def check_waf_rules():
    """WAF設定を確認"""
    print("=== WAF設定確認 ===")
    
    try:
        waf_client = boto3.client('wafv2', region_name='us-east-1')
        
        # WebACLsを取得
        response = waf_client.list_web_acls(Scope='CLOUDFRONT')
        
        if response['WebACLs']:
            for acl in response['WebACLs']:
                print(f"WebACL: {acl['Name']} ({acl['Id']})")
        else:
            print("WAFが設定されていません")
            
    except Exception as e:
        print(f"WAF確認エラー: {e}")

def check_cache_behaviors():
    """Cache Behavior設定を詳細確認"""
    print("\n=== Cache Behavior詳細確認 ===")
    
    distribution_id = "E34ZMEPX9776JV"
    
    try:
        client = boto3.client('cloudfront', region_name='us-east-1')
        response = client.get_distribution(Id=distribution_id)
        config = response['Distribution']['DistributionConfig']
        
        # /api/* behaviorを確認
        for behavior in config['CacheBehaviors']['Items']:
            if behavior['PathPattern'] == '/api/*':
                print("API Behavior設定:")
                print(f"  Allowed Methods: {behavior['AllowedMethods']['Items']}")
                print(f"  Cached Methods: {behavior['AllowedMethods']['CachedMethods']['Items']}")
                print(f"  Viewer Protocol: {behavior['ViewerProtocolPolicy']}")
                print(f"  Origin Request Policy: {behavior.get('OriginRequestPolicyId', 'None')}")
                print(f"  Cache Policy: {behavior.get('CachePolicyId', 'None')}")
                break
                
    except Exception as e:
        print(f"Behavior確認エラー: {e}")

def suggest_fixes():
    """修正提案"""
    print("\n=== 修正提案 ===")
    print("1. CloudFront Behaviorで以下を確認:")
    print("   - Allowed Methods: GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE")
    print("   - Origin Request Policy: CORS-S3Origin または AllViewer")
    print("   - Cache Policy: CachingDisabled (API用)")
    
    print("\n2. WAFルールの確認:")
    print("   - Rate limiting rules")
    print("   - Geographic restrictions")
    print("   - IP whitelist/blacklist")
    
    print("\n3. 手動確認コマンド:")
    print("   aws cloudfront get-distribution --id E34ZMEPX9776JV")
    print("   aws wafv2 list-web-acls --scope CLOUDFRONT")

if __name__ == "__main__":
    print("CloudFront 問題診断...")
    
    check_waf_rules()
    check_cache_behaviors()
    suggest_fixes()
    
    print("\n診断完了")