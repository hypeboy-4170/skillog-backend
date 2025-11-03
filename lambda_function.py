import json
import boto3
from botocore.exceptions import ClientError

cognito = boto3.client('cognito-idp')
ses = boto3.client('ses')

def lambda_handler(event, context):
    try:
        path = event.get('path', '')
        method = event.get('httpMethod', '')
        
        if path == '/login' and method == 'POST':
            return handle_login(event)
        elif path == '/send-email' and method == 'POST':
            return handle_send_email(event)
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def handle_login(event):
    body = json.loads(event['body'])
    username = body['username']
    password = body['password']
    
    try:
        response = cognito.admin_initiate_auth(
            UserPoolId='YOUR_USER_POOL_ID',
            ClientId='YOUR_CLIENT_ID',
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'token': response['AuthenticationResult']['AccessToken']
            })
        }
    except ClientError as e:
        return {
            'statusCode': 401,
            'body': json.dumps({'error': 'Authentication failed'})
        }

def handle_send_email(event):
    headers = event.get('headers', {})
    token = headers.get('Authorization', '').replace('Bearer ', '')
    
    if not verify_token(token):
        return {
            'statusCode': 401,
            'body': json.dumps({'error': 'Unauthorized'})
        }
    
    body = json.loads(event['body'])
    
    try:
        ses.send_email(
            Source='noreply@yourdomain.com',
            Destination={'ToAddresses': [body['to']]},
            Message={
                'Subject': {'Data': body['subject']},
                'Body': {'Text': {'Data': body['message']}}
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Email sent successfully'})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to send email'})
        }

def verify_token(token):
    try:
        cognito.get_user(AccessToken=token)
        return True
    except ClientError:
        return False