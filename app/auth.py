# app/auth.py
import os
import boto3
from botocore.exceptions import ClientError

cognito = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION", "ap-northeast-1"))

USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
CLIENT_ID    = os.getenv("COGNITO_CLIENT_ID")

def sign_up_user(email: str, password: str, name: str):
    try:
        resp = cognito.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "name",  "Value": name}
            ]
        )
        return resp  # UserSub や CodeDeliveryDetails 等が含まれる :contentReference[oaicite:3]{index=3}
    except ClientError as e:
        # エラー処理
        raise

