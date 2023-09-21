import json
import boto3
import os

def handler(event, context):
    try:
        s3 = boto3.client('s3')
        bucket_name = os.environ['BUCKET_NAME']
        object_key = event['queryStringParameters']['file_name']
        expiration = 60*60*5  

        url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration,
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'upload_url': url}),
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

