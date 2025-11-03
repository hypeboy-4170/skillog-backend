import boto3
from botocore.exceptions import ClientError

ses_client = boto3.client('ses', region_name='ap-northeast-1')

def send_email(to_email, subject, body):
    try:
        ses_client.send_email(
            Source='noreply@yourdomain.com',
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
    except ClientError as e:
        raise Exception(f"Failed to send email: {e}")