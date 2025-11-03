import os
import json
import jwt
from jwt import PyJWKClient

def lambda_handler(event, context):
    user_pool_id = os.environ['COGNITO_USER_POOL_ID']
    client_id    = os.environ['COGNITO_CLIENT_ID']
    region       = os.environ.get('REGION', 'ap-northeast-1')

    token = event['headers'].get('Authorization', '').replace('Bearer ', '')
    if not token:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Unauthorized – no token"})
        }

    try:
        jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
        jwks_client = PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        decoded = jwt.decode(token, signing_key.key, algorithms=["RS256"], audience=client_id)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "認証成功", "claims": decoded})
        }

    except Exception as e:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": f"Invalid token: {str(e)}"})
        }
