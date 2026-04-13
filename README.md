# 🛡️ Project Aegis – The Immutable Audit Vault

## 📌 Overview

Project Aegis is a cloud-native file integrity monitoring system designed to ensure authenticity, traceability, and security of uploaded files.

It automatically generates a SHA-256 fingerprint for every file stored in Amazon S3 and maintains a tamper-proof audit trail in DynamoDB. If a file is modified while keeping the same name, the system detects the change and triggers a real-time alert using Amazon SNS.

This project simulates high-stakes environments such as legal, medical, and forensic systems where data integrity is critical.

---

## 🏗️ Architecture

User uploads file
│
▼
Amazon S3 (project-aegis-bucket)
│
▼
S3 Event Trigger
│
▼
AWS Lambda (Hash Function)
│
┌────┴─────────────┐
▼ ▼
DynamoDB SNS Topic
(Store hash) (Send alert)
│ │
▼ ▼
Compare hashes Email Notification

---

## ⚙️ Technical Stack

- Amazon S3 – Object storage with event triggers  
- AWS Lambda (Python) – Serverless compute for hashing and logic  
- Python (hashlib, boto3) – SHA-256 hashing and AWS SDK  
- Amazon DynamoDB – Stores file metadata and hash history  
- Amazon SNS – Sends real-time email alerts  
- Amazon CloudWatch – Logging and monitoring  
- IAM Roles & Policies – Secure service permissions  

---

## 🔄 Workflow

1. User uploads a file to Amazon S3  
2. S3 triggers the Lambda function  
3. Lambda:
   - Retrieves the file
   - Generates SHA-256 hash
   - Queries DynamoDB for previous hash
4. If hash is different:
   - Sends alert via SNS
5. Stores new hash in DynamoDB  

---

## 🔐 Security Logic

- Same filename + different content = 🚨 ALERT  
- Same filename + same content = ✅ No alert  

---

## 🧪 Testing Scenario

### Step 1
Upload file:
test.txt → hello


### Step 2
Modify file:
test.txt → HELLO WORLD 123456


### Result
- Hash changes  
- SNS email alert triggered  
- DynamoDB updated  

---

## 🧠 Key Features
- Serverless architecture  
- Real-time event-driven processing  
- File integrity verification using SHA-256  
- Automated alerting system  
- Historical tracking using DynamoDB  

---

## 📂 Project Structure

project-aegis/
│
├── lambda/
│ └── lambda_function.py
│
├── architecture/
│ └── diagram.png
│
├── screenshots/
│ ├── s3-upload.png
│ ├── dynamodb.png
│ ├── cloudwatch.png
│ └── sns-alert.png
│
└── README.md
## 🔑 IAM Permissions Required

```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:ListBucket",
    "dynamodb:PutItem",
    "dynamodb:Query",
    "sns:Publish"
  ],
  "Resource": "*"
}
```

## 🔑 IAM Permissions Required (Lambda Role)

This policy allows Lambda to:
- Read files from S3
- Store hashes in DynamoDB
- Send alerts via SNS

## 📸 Screenshots

### S3 Upload Trigger
![S3](screenshots/s3-upload.png)

### DynamoDB Records
![DynamoDB](screenshots/dynamodb.png)

### CloudWatch Logs
![Logs](screenshots/cloudwatch.png)

### SNS Alert Email
![SNS](screenshots/sns-alert.png)<img width="1536" height="1024" alt="Project Aegis_ file monitoring flowchart" src="https://github.com/user-attachments/assets/9068443b-5e7c-49ff-b5b6-0feb52a0eabb" />
<img width="1536" height="1024" alt="Project Aegis_ file monitoring flowchart" src="https://github.com/user-attachments/assets/1e36eb38-b177-4a3e-9ef5-df56e2ac5ff4" />
