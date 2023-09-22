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
        id = request_body['id']
        file_data = request_body['file_data']

        s3.put_object(
            Bucket=bucket_name,
            Key=id,
            Body=file_data,
        )

        response = table.put_item(
            Item={
                'id': id,
                'file_data': file_data
            }
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'File uploaded and data inserted into DynamoDB successfully'}),
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Error uploading file or inserting data into DynamoDB'}),
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
