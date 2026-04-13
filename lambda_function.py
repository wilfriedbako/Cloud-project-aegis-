import boto3
import hashlib
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

table = dynamodb.Table('aegis-audit-table')

SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:490848272326:Project-aegis-alerts'

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Bucket: {bucket}")
    print(f"File: {key}")

    obj = s3.get_object(Bucket=bucket, Key=key)

    sha256 = hashlib.sha256()
    for chunk in obj['Body'].iter_chunks():
        sha256.update(chunk)

    file_hash = sha256.hexdigest()
    timestamp = datetime.utcnow().isoformat()

    print(f"SHA256: {file_hash}")

    # 🔎 Check if file already exists
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('file_name').eq(key)
    )

    items = response.get('Items', [])

    # 🚨 Compare hashes
    if items:
        last_hash = items[-1]['hash']

        if last_hash != file_hash:
            print("⚠️ Possible tampering detected!")

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="🚨 File Integrity Alert",
                Message=f"File {key} has been modified!\nOld hash: {last_hash}\nNew hash: {file_hash}"
            )

    # 💾 Save new record
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
