import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def handler(event, context):
    try:
        s3 = boto3.client('s3')
        bucket_name = os.environ['BUCKET_NAME']
        request_body = json.loads(event['body'])
        file_name = request_body['file_name']
        file_data = request_body['file_data']

        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_data,
        )

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
