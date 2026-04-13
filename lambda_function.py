import boto3
import hashlib
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('aegis-audit-table')

def lambda_handler(event, context):

    # Get bucket and file
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Bucket: {bucket}")
    print(f"File: {key}")

    # Get file
    obj = s3.get_object(Bucket=bucket, Key=key)

    # Hash file
    sha256 = hashlib.sha256()
    for chunk in obj['Body'].iter_chunks():
        sha256.update(chunk)

    file_hash = sha256.hexdigest()
    timestamp = datetime.utcnow().isoformat()

    print(f"SHA256: {file_hash}")

    # Save to DynamoDB
    table.put_item(
        Item={
            'file_name': key,
            'timestamp': timestamp,
            'hash': file_hash,
            'bucket': bucket
        }
    )

    print("Saved to DynamoDB")

    return {
        "statusCode": 200,
        "body": file_hash
    }
