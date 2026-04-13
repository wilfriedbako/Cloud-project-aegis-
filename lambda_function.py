import boto3
import hashlib
from datetime import datetime
from boto3.dynamodb.conditions import Key

# AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Resources
table = dynamodb.Table('aegis-audit-table')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:490848272326:Project-aegis-alerts'


def lambda_handler(event, context):

    # Get bucket and file info
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Bucket: {bucket}")
    print(f"File: {key}")

    # Get file from S3
    obj = s3.get_object(Bucket=bucket, Key=key)

    # Generate SHA-256 hash
    sha256 = hashlib.sha256()
    for chunk in obj['Body'].iter_chunks():
        sha256.update(chunk)

    file_hash = sha256.hexdigest()
    print("New hash:", file_hash)

    # 🔥 STEP 1: GET OLD RECORDS (BEFORE saving new one)
    response = table.query(
        KeyConditionExpression=Key('file_name').eq(key)
    )

    items = response.get('Items', [])
    print("All items:", items)

    # 🔥 STEP 2: COMPARE HASHES (if previous exists)
    if items:
        sorted_items = sorted(items, key=lambda x: x['timestamp'])
        last_hash = sorted_items[-1]['hash']

        print("Last hash:", last_hash)

        if last_hash != file_hash:
            print("🚨 Tampering detected!")

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="🚨 File Integrity Alert",
                Message=f"""
File tampering detected!

File: {key}
Bucket: {bucket}

Old Hash: {last_hash}
New Hash: {file_hash}

Time: {datetime.utcnow().isoformat()}
"""
            )

    # 🔥 STEP 3: SAVE NEW RECORD (AFTER comparison)
    table.put_item(
        Item={
            'file_name': key,
            'timestamp': datetime.utcnow().isoformat(),
            'hash': file_hash,
            'bucket': bucket
        }
    )

    return {
        "statusCode": 200,
        "body": file_hash
    }
