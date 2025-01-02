import boto3
import os
import logging
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def log_to_dynamodb(file_name, message):
    try:
        dynamodb = boto3.resource('dynamodb')
        table_name = os.environ['DYNAMODB_TABLE']
        table = dynamodb.Table(table_name)

        response = table.put_item(
            Item={
                'file_name': file_name,
                'log_message': message
            }
        )
        logger.info(f"Log entry added to DynamoDB for file: {file_name}")
    except Exception as e:
        logger.error(f"Error logging to DynamoDB: {str(e)}")

def check_file(file_name, bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.head_object(Bucket=bucket_name, Key=file_name)
        file_size = response['ContentLength']

        if file_size == 0:
            log_to_dynamodb(file_name, "File size is 0.")
            return "File size is 0. Logged in DB."

        file_object = s3.get_object(Bucket=bucket_name, Key=file_name)
        file_body = file_object['Body'].read(10)  # Read the first 10 bytes to check if the file can be opened
        
        if not file_body:
            log_to_dynamodb(file_name, "File is not opened.")
            return "File cannot be opened. Logged in DB."

        return "File processed successfully."

    except ClientError as e:
        logger.error(f"Error accessing file {file_name}: {str(e)}")
        log_to_dynamodb(file_name, f"Error accessing file: {str(e)}")
        return "Error accessing file. Logged in DB."

def lambda_handler(event, context):
    bucket_name = event.get('bucket_name')
    files = event.get('files', [])

    if not bucket_name or not files:
        return {
            'statusCode': 400,
            'message': "Missing bucket name or file list in the input event."
        }

    results = {}
    for file_name in files:
        results[file_name] = check_file(file_name, bucket_name)

    return {
        'statusCode': 200,
        'message': "File processing completed.",
        'results': results
    }
