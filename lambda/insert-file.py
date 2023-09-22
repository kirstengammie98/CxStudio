import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def handler(event, context):
    try:
        s3_event = event['Records'][0]['s3']
        bucket_name = s3_event['bucket']['name']
        object_key = s3_event['object']['key']

        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_data = response['Body'].read()

        file_content = json.loads(file_data)

        response = table.put_item(
            Item={
                'file_name': 'file_name',  
                'file_data': file_content 
            }
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Data inserted into DynamoDB successfully'}),
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Error inserting data into DynamoDB'}),
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
