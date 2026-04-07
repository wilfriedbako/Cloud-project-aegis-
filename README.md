# Project Aegis – The Immutable Audit Vault 🔒

## Overview
Project Aegis is a cloud-native solution that ensures file integrity and traceability. It automatically fingerprints and locks every uploaded file, creating a tamper proof audit trail. Built with AWS serverless services, this project is designed for high stakes environments like legal, medical, or forensic data.

## Technical Stack
- **AWS S3** – Object storage with Versioning and Object Lock  
- **AWS Lambda** – Automates file fingerprinting  
- **Python (hashlib)** – SHA-256 hashing for file integrity  
- **AWS DynamoDB** – Stores metadata and audit trail  
- **AWS SNS** – Sends alerts on suspicious changes  

## Workflow
1. **Vault Creation:** S3 bucket with Versioning and Object Lock.  
2. **Digital Fingerprint:** Lambda calculates SHA-256 hash on every upload.  
3. **Audit Ledger:** DynamoDB stores Filename, Hash, Uploader, Timestamp.  
4. **Integrity Alert:** SNS alerts security team if a file is modified.

## Key Skills Demonstrated
- Cloud architecture with AWS serverless services  
- Automation using Lambda & Python  
- Data integrity and security  
- Event driven monitoring and alerting  

## Elevator Pitch
> “Project Aegis is a secure cloud system that automatically locks and tracks files so they can’t be altered, ensuring the data is always authentic and trustworthy even in high stakes environments.”
