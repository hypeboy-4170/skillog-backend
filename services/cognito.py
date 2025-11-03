import boto3
from botocore.exceptions import ClientError

cognito_client = boto3.client('cognito-idp', region_name='ap-northeast-1')

USER_POOL_ID = 'ap-northeast-1_WncgvrLUL'
CLIENT_ID = '5ba0ae4io3vsdp5i574tfevo7a'

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
        response = cognito_client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
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