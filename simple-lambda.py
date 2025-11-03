import json
import boto3
import os
from botocore.exceptions import ClientError

# Cognito と SES クライアント
cognito = boto3.client('cognito-idp', region_name='ap-northeast-1')
ses = boto3.client('ses', region_name='ap-northeast-1')

USER_POOL_ID = os.environ.get('USER_POOL_ID', 'ap-northeast-1_WncgvrLUL')
CLIENT_ID = os.environ.get('CLIENT_ID', '5ba0ae4io3vsdp5i574tfevo7a')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', '1cf7q4beajh4jjcqm04os3hkqbe7mbp6gdv46qrgd3esegrkj1hi')

def lambda_handler(event, context):
    try:
        path = event.get('path', '')
        method = event.get('httpMethod', '')
        
        # CORS ヘッダー
        headers = {
            'Access-Control-Allow-Origin': 'https://allforone-freesite.com',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        }
        
        if method == 'OPTIONS':
            return {'statusCode': 200, 'headers': headers, 'body': ''}
        
        if path == '/register' and method == 'POST':
            return handle_register(event, headers)
        elif path == '/login' and method == 'POST':
            return handle_login(event, headers)
        elif path == '/sendmail' and method == 'POST':
            return handle_sendmail(event, headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def handle_register(event, headers):
    body = json.loads(event['body'])
    username = body['username']
    password = body['password']
    email = body['email']
    
    try:
        import hmac
        import hashlib
        import base64
        
        # CLIENT_SECRET用のSECRET_HASHを計算
        message = username + CLIENT_ID
        secret_hash = base64.b64encode(hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).digest()).decode()
        
        cognito.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=username,
            TemporaryPassword=password,
            UserAttributes=[{'Name': 'email', 'Value': email}],
            MessageAction='SUPPRESS'
        )
        cognito.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=username,
            Password=password,
            Permanent=True
        )
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'User created successfully'})
        }
    except ClientError as e:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def handle_login(event, headers):
    body = json.loads(event['body'])
    username = body['username']
    password = body['password']
    
    print(f"Login attempt for user: {username}")
    print(f"Using UserPool: {USER_POOL_ID}")
    print(f"Using ClientId: {CLIENT_ID}")
    
    try:
        import hmac
        import hashlib
        import base64
        
        # CLIENT_SECRET用のSECRET_HASHを計算
        message = username + CLIENT_ID
        secret_hash = base64.b64encode(hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).digest()).decode()
        
        response = cognito.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username, 
                'PASSWORD': password,
                'SECRET_HASH': secret_hash
            }
        )
        print("Login successful")
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'access_token': response['AuthenticationResult']['AccessToken']})
        }
    except ClientError as e:
        print(f"Login error: {str(e)}")
        return {
            'statusCode': 401,
            'headers': headers,
            'body': json.dumps({'error': 'Authentication failed'})
        }

def handle_sendmail(event, headers):
    auth_header = event.get('headers', {}).get('Authorization', '')
    token = auth_header.replace('Bearer ', '')
    
    if not verify_token(token):
        return {
            'statusCode': 401,
            'headers': headers,
            'body': json.dumps({'error': 'Unauthorized'})
        }
    
    body = json.loads(event['body'])
    
    try:
        ses.send_email(
            Source='noreply@allforone-freesite.com',
            Destination={'ToAddresses': [body['to']]},
            Message={
                'Subject': {'Data': body['subject']},
                'Body': {'Text': {'Data': body['body']}}
            }
        )
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Email sent successfully'})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Failed to send email'})
        }

def verify_token(token):
    try:
        cognito.get_user(AccessToken=token)
        return True
    except ClientError:
        return False