const { Stack, Duration } = require('aws-cdk-lib');
const { RestApi, LambdaIntegration } = require('aws-cdk-lib/aws-apigateway');
const { Bucket } = require('aws-cdk-lib/aws-s3');
const { Function, Runtime, Code } = require('aws-cdk-lib/aws-lambda');
const { Table, AttributeType } = require('aws-cdk-lib/aws-dynamodb');    
const { Policy, PolicyStatement, Effect } = require('aws-cdk-lib/aws-iam');
const { Role, ServicePrincipal } = require('aws-cdk-lib/aws-iam');


class CdkprojectStack extends Stack {
  constructor(scope, id, props) {
    super(scope, id, props);

    const s3Bucket = new Bucket(this, 'S3Bucket');

    const dynamoDBTable = new Table(this, 'DynamoDBTable', {
      partitionKey: { name: 'id', type: AttributeType.STRING },
    });

    const lambdaFunction = new Function(this, 'LambdaFunction', {
      runtime: Runtime.PYTHON_3_8, 
      handler: 'lambda.lambda_handler', 
      code: Code.fromAsset('lambda'),
      timeout: Duration.seconds(30),
      environment: {
        BUCKET_NAME: s3Bucket.bucketName,
        TABLE_NAME: dynamoDBTable.tableName,
      },
    });

    s3Bucket.grantRead(lambdaFunction);
    dynamoDBTable.grantReadWriteData(lambdaFunction);

    const apiRole = new Role(this, 'ApiGatewayRole', {
      assumedBy: new ServicePrincipal('apigateway.amazonaws.com'),
    });
    
    const s3Policy = new Policy(this, 'S3Policy', {
      statements: [
        new PolicyStatement({
          actions: ['s3:PutObject', 's3:GetObject'],
          effect: Effect.ALLOW,
          resources: [s3Bucket.bucketArn + '/*'],
        }),
      ],
    });
    apiRole.attachInlinePolicy(s3Policy);

    const api = new RestApi(this, 'Api', {deploy: true,});
    const apiIntegration = new LambdaIntegration(lambdaFunction);
    const apiResource = api.root.addResource('upload');
    apiResource.addMethod('POST', apiIntegration);
  }
}

module.exports = { CdkprojectStack };
