import boto3
import hashlib
import urllib.parse
from datetime import datetime
from boto3.dynamodb.conditions import Key

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

table = dynamodb.Table('aegis-audit-table')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:490848272326:Project-aegis-alerts'

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    print("Bucket:", bucket)
    print("File:", key)

    obj = s3.get_object(Bucket=bucket, Key=key)

    sha256 = hashlib.sha256()
    for chunk in obj['Body'].iter_chunks():
        sha256.update(chunk)

    file_hash = sha256.hexdigest()
    print("New hash:", file_hash)

    # Get old records
    response = table.query(
        KeyConditionExpression=Key('file_name').eq(key)
    )
    items = response.get('Items', [])

    # Compare
    if items:
        items = sorted(items, key=lambda x: x['timestamp'])
        last_hash = items[-1]['hash']

        if last_hash != file_hash:
            print("🚨 Tampering detected!")

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="File Integrity Alert",
                Message=f"{key} changed!\nOld: {last_hash}\nNew: {file_hash}"
            )

    # Save new record
    table.put_item(
        Item={
            'file_name': key,
            'timestamp': datetime.utcnow().isoformat(),
            'hash': file_hash,
            'bucket': bucket
        }
    )

    print("Saved to DynamoDB")

    return {"statusCode": 200}
