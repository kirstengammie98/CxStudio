# README

# CDK Deployment for API Gateway, S3, Lambda, and DynamoDB

This project creates a CDK deployment that provisions an AWS API Gateway, S3 Bucket, Lambda function, and DynamoDB table. The deployment allows users to upload files to S3 using the API and insert data from the uploaded files into the DynamoDB table.

## Prerequisites

Ensure you have the following prerequisites installed and configured:

- [Node.js and npm](https://nodejs.org/) (Node.js version >= 14)
- [AWS CLI](https://aws.amazon.com/cli/) and configure it with your AWS credentials/
- [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) installed globally by running: `npm install -g aws-cdk`

## Setup

Follow these steps to set up your development environment and deploy the CDK stack:

1. ### Clone the repository to your local machine:

   ```bash
   git clone https://github.com/kirstengammie98/CxStudio.git
   cd CxStudio
   ```

2.  ### Install Dependencies:

      ```bash
      npm install
      ```

3. ### Deploy the CDK Stack:

   Navigate to the project directory and use the following command:

   ```bash
   cdk deploy
   ```

   Make note of the output values, such as the API Gateway URL, which you will use to interact with the API.

4. ### Usage:

   Once the CDK stack is deployed, you can use the following endpoints:

   #### `*` Generate URL Endpoint (GET)

   To generate a pre-signed URL for uploading a file to the S3 bucket, you can use the API endpoint that was generated after deployment.

   ```python
   if __name__ == "__main__":
      file_name = "example.txt"
      file_data = b"Hello, World!" 
      generate_url_endpoint = "YOUR_GENERATE_URL_ENDPOINT_HERE"
      upload_file(file_name, file_data, generate_url_endpoint)
   ```

   Replace `"YOUR_GENERATE_URL_ENDPOINT_HERE"` with the actual URL of your API Gateway's /generate-url resource.

   Make sure to have the necessary Python packages (requests, boto3) installed for your client script to work.

5. ### Run the Python Client:

   Run the Python client `upload_script.py` to upload a file to the S3 bucket using the generated pre-signed URL:

   ```bash
   python client_upload_file.py
   ```