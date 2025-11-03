#!/usr/bin/env python3
import boto3
import json

def fix_cloudfront_behavior():
    """CloudFront Behaviorの優先順位を修正"""
    print("=== CloudFront Behavior修正 ===")
    
    distribution_id = "E34ZMEPX9776JV"
    
    try:
        client = boto3.client('cloudfront', region_name='us-east-1')
        
        # 現在の設定を取得
        response = client.get_distribution_config(Id=distribution_id)
        config = response['DistributionConfig']
        etag = response['ETag']
        
        print("現在のBehavior設定:")
        print(f"Default: {config['DefaultCacheBehavior']['TargetOriginId']}")
        
        for i, behavior in enumerate(config['CacheBehaviors']['Items']):
            print(f"  {i}: {behavior['PathPattern']} -> {behavior['TargetOriginId']}")
        
        # /api/* behaviorを最初に移動（優先順位を上げる）
        behaviors = config['CacheBehaviors']['Items']
        api_behavior = None
        other_behaviors = []
        
        for behavior in behaviors:
            if behavior['PathPattern'] == '/api/*':
                api_behavior = behavior
            else:
                other_behaviors.append(behavior)
        
        if api_behavior:
            # API behaviorを最初に配置
            config['CacheBehaviors']['Items'] = [api_behavior] + other_behaviors
            
            print("\n修正後のBehavior順序:")
            for i, behavior in enumerate(config['CacheBehaviors']['Items']):
                print(f"  {i}: {behavior['PathPattern']} -> {behavior['TargetOriginId']}")
            
            # 設定を更新
            client.update_distribution(
                Id=distribution_id,
                DistributionConfig=config,
                IfMatch=etag
            )
            
            print("\n✅ CloudFront設定を更新しました")
            print("⏳ 変更の反映には5-10分かかります")
        else:
            print("❌ /api/* behaviorが見つかりません")
            
    except Exception as e:
        print(f"❌ 修正エラー: {e}")

def create_manual_fix_commands():
    """手動修正用のコマンドを生成"""
    print("\n=== 手動修正コマンド ===")
    
    commands = """
# 1. 現在の設定をバックアップ
aws cloudfront get-distribution-config --id E34ZMEPX9776JV > backup-config.json

# 2. ETagを取得
ETAG=$(jq -r '.ETag' backup-config.json)

# 3. /api/* behaviorを最優先に設定
jq '.DistributionConfig.CacheBehaviors.Items |= 
  (map(select(.PathPattern == "/api/*")) + map(select(.PathPattern != "/api/*"))) |
  del(.ETag)' backup-config.json > fixed-config.json

# 4. 設定を適用
aws cloudfront update-distribution \\
  --id E34ZMEPX9776JV \\
  --distribution-config file://fixed-config.json \\
  --if-match $ETAG

# 5. 状態確認
aws cloudfront get-distribution --id E34ZMEPX9776JV --query 'Distribution.Status'
"""
    
    print(commands)

if __name__ == "__main__":
    print("CloudFront ルーティング修正...")
    
    fix_cloudfront_behavior()
    create_manual_fix_commands()
    
    print("\n修正完了")