import json

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    username = body.get('username', '').strip()
    password = body.get('password', '').strip()
    
    if not username or not password:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'IDとパスワードを入力してください'})
        }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'success': True})
    }
