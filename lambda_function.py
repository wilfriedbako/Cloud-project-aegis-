import boto3
import hashlib

s3 = boto3.client('s3')

def lambda_handler(event, context):

    # Get bucket + file from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Bucket: {bucket}")
    print(f"File: {key}")

    # Get file from S3
    obj = s3.get_object(Bucket=bucket, Key=key)

    # Hash file
    sha256 = hashlib.sha256()
    for chunk in obj['Body'].iter_chunks():
        sha256.update(chunk)

    file_hash = sha256.hexdigest()

    print(f"SHA256: {file_hash}")

    return {
        "statusCode": 200,
        "body": file_hash
    }
