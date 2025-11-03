#!/usr/bin/env python3
import boto3
import sys

def check_user(username):
    """Cognitoユーザーの状態を確認"""
    user_pool_id = 'ap-northeast-1_WncgvrLUL'
    
    try:
        client = boto3.client('cognito-idp', region_name='ap-northeast-1')
        
        # ユーザー情報を取得
        response = client.admin_get_user(
            UserPoolId=user_pool_id,
            Username=username
        )
        
        print(f"ユーザー: {username}")
        print(f"状態: {response['UserStatus']}")
        print(f"有効: {response['Enabled']}")
        
        print("属性:")
        for attr in response['UserAttributes']:
            print(f"  {attr['Name']}: {attr['Value']}")
            
        return True
        
    except client.exceptions.UserNotFoundException:
        print(f"ユーザー '{username}' が見つかりません")
        return False
    except Exception as e:
        print(f"エラー: {e}")
        return False

def create_test_user(username, password):
    """テストユーザーを作成"""
    user_pool_id = 'ap-northeast-1_WncgvrLUL'
    
    try:
        client = boto3.client('cognito-idp', region_name='ap-northeast-1')
        
        # ユーザー作成
        client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            TemporaryPassword=password,
            MessageAction='SUPPRESS'
        )
        
        # パスワードを永続化
        client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password=password,
            Permanent=True
        )
        
        print(f"ユーザー '{username}' を作成しました")
        return True
        
    except Exception as e:
        print(f"ユーザー作成エラー: {e}")
        return False

if __name__ == "__main__":
    username = "testuser7"
    password = "TestPass123!"
    
    print("=== Cognitoユーザー確認 ===")
    
    if not check_user(username):
        print(f"\n=== ユーザー '{username}' を作成 ===")
        if create_test_user(username, password):
            check_user(username)