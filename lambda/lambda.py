import os
import json
import boto3
import uuid

table_name = os.environ['TABLE_NAME']
bucket_name = os.environ['BUCKET_NAME']
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
      body = json.loads(event['body'])
      name = body['name']
      content_type = body['contentType']
      file_data = event['headers']['x-file']
      
      file_id = str(uuid.uuid4())


      s3_client.put_object(
          Bucket=bucket_name,
          Key=file_id,
          Body=file_data,
          ContentType=content_type
      )

      dynamo_table = dynamodb.Table(table_name)
      dynamo_table.put_item(
          Item={
              'fileId': file_id,
              'name': name,
              'contentType': content_type,
              'createdAt': str(context.aws_request_time),
          }
      )

      return {
          'statusCode': 200,
          'body': json.dumps('Data inserted into DynamoDB successfully')
      }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }