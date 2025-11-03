import boto3
import hmac
import hashlib
import base64
from botocore.exceptions import ClientError

cognito_client = boto3.client('cognito-idp', region_name='ap-northeast-1')

USER_POOL_ID = 'ap-northeast-1_WncgvrLUL'
CLIENT_ID = '5ba0ae4io3vsdp5i574tfevo7a'
CLIENT_SECRET = None  # 環境変数から取得するか、設定が必要

def get_secret_hash(username):
    if not CLIENT_SECRET:
        return None
    message = username + CLIENT_ID
    dig = hmac.new(CLIENT_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

def create_user(username, password, email):
    try:
        cognito_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=username,
            TemporaryPassword=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email}
            ],
            MessageAction='SUPPRESS'
        )
        cognito_client.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=username,
            Password=password,
            Permanent=True
        )
    except ClientError as e:
        raise Exception(f"Failed to create user: {e}")

def authenticate_user(username, password):
    try:
        auth_params = {
            'USERNAME': username,
            'PASSWORD': password
        }
        
        # SECRET_HASHが必要な場合は追加
        secret_hash = get_secret_hash(username)
        if secret_hash:
            auth_params['SECRET_HASH'] = secret_hash
        
        response = cognito_client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters=auth_params
        )
        return response['AuthenticationResult']['AccessToken']
    except ClientError as e:
        raise Exception(f"Authentication failed: {e}")

def verify_token(token):
    try:
        cognito_client.get_user(AccessToken=token)
        return True
    except ClientError:
        return False