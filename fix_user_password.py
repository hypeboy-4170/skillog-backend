#!/usr/bin/env python3
import boto3
import os

# 実際のCLIENT_SECRETを設定
os.environ['CLIENT_SECRET'] = '1cf7q4beajh4jjcqm04os3hkqbe7mbp6gdv46qrgd3esegrkj1hi'

def reset_user_password():
    """ユーザーパスワードをリセット"""
    user_pool_id = 'ap-northeast-1_WncgvrLUL'
    username = "testuser7"
    new_password = "TestPass123!"
    
    try:
        client = boto3.client('cognito-idp', region_name='ap-northeast-1')
        
        # パスワードをリセット
        client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password=new_password,
            Permanent=True
        )
        
        print(f"パスワードをリセットしました: {username}")
        return True
        
    except Exception as e:
        print(f"パスワードリセットエラー: {e}")
        return False

def test_login():
    """ログインテスト"""
    import sys
    sys.path.append('services')
    from cognito import authenticate_user
    
    try:
        token = authenticate_user("testuser7", "TestPass123!")
        print(f"ログイン成功: {token[:50]}...")
        return True
    except Exception as e:
        print(f"ログイン失敗: {e}")
        return False

if __name__ == "__main__":
    print("=== ユーザーパスワード修正 ===")
    
    if reset_user_password():
        print("\n=== ログインテスト ===")
        test_login()