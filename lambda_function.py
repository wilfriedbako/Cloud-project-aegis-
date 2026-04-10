import hashlib

def lambda_handler(event, context):
    file_content = "sample data"

    file_hash = hashlib.sha256(file_content.encode()).hexdigest()

    print("File received")
    print("SHA256 Hash:", file_hash)

    return {
        "statusCode": 200,
        "body": file_hash
    }