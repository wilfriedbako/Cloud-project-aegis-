**Project Aegis – The Immutable Audit Vault** 
**Overview**
Project Aegis is a cloud native solution that ensures file integrity and traceability. It automatically fingerprints and locks every uploaded file, creating a tamper proof audit trail. Built with AWS serverless services, this project simulates high stakes environments like legal, medical, or forensic data, where accuracy and reliability are critical.

**Technical Stack**
• AWS S3 – Object storage with Versioning and Object Lock
• AWS Lambda – Automates file fingerprinting
• Python (hashlib) – SHA-256 hashing for file integrity
• AWS DynamoDB – Stores metadata and audit trail
• AWS SNS – Sends alerts on suspicious changes
• Infrastructure as Code – Terraform / CloudFormation for reproducible deployment

**Workflow / Steps **
• Vault Creation: S3 bucket with Versioning and Object Lock to ensure file history is never lost.
• Digital Fingerprint: Lambda calculates SHA-256 hash on every upload to detect tampering.
• Audit Ledger: DynamoDB stores Filename, Hash, Uploader, and Timestamp to create an immutable record.
• Integrity Alert: SNS alerts the security team if a file is modified, enabling proactive action.

**Real World Challenges Solved **
• Problem: High concurrency uploads caused some DynamoDB writes to fail.
• Root Cause: DynamoDB table provisioned throughput limits were exceeded.
• Troubleshooting: Monitored CloudWatch metrics, reviewed write capacity and request patterns.
• Solution: Enabled auto scaling and added retry logic in Lambda functions.
• Result: All uploads now reliably create audit entries, even under heavy load.

•** Duplicate File Alerts**
• Problem: Users uploaded files with the same name, causing false alerts.
• Root Cause: Alert system compared filenames only, ignoring file content.
• Troubleshooting: Tested file uploads with duplicate names but different content.
• Solution: Updated Lambda to compare SHA-256 hashes before triggering alerts.
• Result: Only genuine tampering events generate alerts, reducing noise.

**• S3 Object Lock Misconfiguration**
• Problem: Older file versions could still be overwritten accidentally.
• Root Cause: Bucket Object Lock settings were not set to Compliance Mode.
• Troubleshooting: Reviewed S3 bucket policies, tested uploads, checked version history.
• Solution: Enabled Compliance Mode with versioning on all buckets.
• Result: Files cannot be deleted or overwritten during retention period, ensuring legal grade immutability.

**• Lambda Timeout on Large File Uploads**
• Problem: Large files sometimes caused Lambda to timeout before hash calculation completed.
• Root Cause: Lambda function had a default timeout too short for large files.
• Troubleshooting: Simulated uploads with increasing file sizes, monitored execution duration.
• Solution: Increased Lambda timeout, refactored code to read files in streaming chunks.
• Result: Even very large files are processed successfully, maintaining integrity checks without errors.

**Key Skills Demonstrated **
• Cloud architecture design with AWS serverless services
• Automation and even driven programming with Lambda & Python
• Data integrity and tamper proof audit logging

**Elevator Pitch **
Project Aegis is more than a secure file system. I built it to handle real-world challenges like DynamoDB throttling, duplicate alerts, object lock misconfigurations, and large file timeouts. This ensures files are always authentic, traceable, and tamper-proof. It demonstrates my ability to solve complex cloud problems with automation, reliability, and security
• Monitoring, alerting, and proactive security measures
• Troubleshooting real-world issues under complex scenarios
• Reproducible deployment using Infrastructure as Code
