const { Stack, Duration } = require('aws-cdk-lib');
const { RestApi, LambdaIntegration } = require('aws-cdk-lib/aws-apigateway');
const { Bucket } = require('aws-cdk-lib/aws-s3');
const { Function, Runtime, Code } = require('aws-cdk-lib/aws-lambda');
const { Table, AttributeType } = require('aws-cdk-lib/aws-dynamodb');    
const { S3EventSource } = require('aws-cdk-lib/aws-lambda-event-sources');  


class CdkprojectStack extends Stack {
  constructor(scope, id, props) {
    super(scope, id, props);

    const s3Bucket = new Bucket(this, 'S3Bucket');
    const dynamoDBTable = new Table(this, 'DBTable', {
      partitionKey: { name: 'file_name', type: AttributeType.STRING },
    });

    const uploadFileLambda = new Function(this, 'UploadFileLambda', {
      runtime: Runtime.PYTHON_3_8, 
      handler: 'upload-file.handler', 
      code: Code.fromAsset('lambda'),
      timeout: Duration.seconds(90),
      environment: {
        BUCKET_NAME: s3Bucket.bucketName,
        TABLE_NAME: dynamoDBTable.tableName,
      },
    });

    const generateUrlLambda = new Function(this, 'GenerateUrlLambda', {
      runtime: Runtime.PYTHON_3_8,
      handler: 'generate-url.handler',
      code: Code.fromAsset('lambda'),
      timeout: Duration.seconds(90),
      environment: {
        BUCKET_NAME: s3Bucket.bucketName,
        TABLE_NAME: dynamoDBTable.tableName,
      },
    });

    const insertFileLambda = new Function(this, 'InsertFileLambda', {
      runtime: Runtime.PYTHON_3_8, 
      handler: 's3-to-insert-file.handler', 
      code: Code.fromAsset('lambda'),
      timeout: Duration.seconds(90),
      environment: {
        TABLE_NAME: dynamoDBTable.tableName,
      },
    });

    insertFileLambda.addEventSource(new S3EventSource(s3Bucket, {
      events: [ 's3:ObjectCreated:*' ], 
    }));

    s3Bucket.grantReadWrite(uploadFileLambda);
    dynamoDBTable.grantReadWriteData(uploadFileLambda);
    s3Bucket.grantReadWrite(generateUrlLambda);
    dynamoDBTable.grantReadWriteData(generateUrlLambda);
    s3Bucket.grantRead(insertFileLambda);
    dynamoDBTable.grantReadWriteData(insertFileLambda);

    const api = new RestApi(this, 'Api', { deploy: true });

    const uploadFileIntegration = new LambdaIntegration(uploadFileLambda);
    const uploadResource = api.root.addResource('upload');
    uploadResource.addMethod('POST', uploadFileIntegration);

    const generateUrlIntegration = new LambdaIntegration(generateUrlLambda);
    const generateResource = api.root.addResource('generate-url');
    generateResource.addMethod('GET', generateUrlIntegration);

  }
}

module.exports = { CdkprojectStack };
