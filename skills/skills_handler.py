import json

def lambda_handler(event, context):
    general_skills = [
        {'id': 1, 'name': 'Python', 'level': 5},
        {'id': 2, 'name': 'JavaScript', 'level': 4},
        {'id': 3, 'name': 'AWS', 'level': 3},
        {'id': 4, 'name': 'TypeScript', 'level': 2}
    ]
    
    specialized_skills = [
        {'id': 's1', 'name': 'コンテナ基盤', 'level': 1},
        {'id': 's2', 'name': '開発環境', 'level': 1},
        {'id': 's3', 'name': 'Webシステム基盤', 'level': 1},
        {'id': 's4', 'name': '大樹生命ビジネスの理解', 'level': 1}
    ]
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'generalSkills': general_skills,
            'specializedSkills': specialized_skills
        })
    }
