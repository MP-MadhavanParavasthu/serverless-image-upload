# AWS Serverless Image Upload API
A serverless image upload and retrieval application built using AWS cloud services and Python.

## Project Overview
This project demonstrates how to build a serverless backend for storing images and managing image metadata without maintaining traditional servers.
It uses Amazon API Gateway to expose HTTP endpoints, AWS Lambda to process requests, Amazon S3 to store images, Amazon DynamoDB to manage metadata, and Amazon CloudWatch for monitoring.

## AWS Services Used
- **Amazon API Gateway** — Provides HTTP API endpoints.
- **AWS Lambda** — Executes backend logic using Python.
- **Amazon S3** — Stores uploaded images.
- **Amazon DynamoDB** — Stores image metadata.
- **Amazon CloudWatch** — Captures logs for troubleshooting.
- **AWS IAM** — Manages permissions between AWS services.

## Architecture
Client → API Gateway → AWS Lambda → Amazon S3 / DynamoDB
AWS Lambda → Amazon CloudWatch Logs

## Features
- Serverless image upload API
- Image storage using Amazon S3
- Image metadata management using DynamoDB
- Image retrieval through an HTTP API
- CloudWatch logging and monitoring
- IAM-based access to AWS resources

## API Endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/upload` | Upload an image |
| GET | `/images` | Retrieve image information |

## Technologies
Python, AWS Lambda, API Gateway, Amazon S3, DynamoDB, CloudWatch, IAM, AWS CLI and Git.

## Project Outcome
Successfully developed and tested an AWS serverless application that accepts image uploads, stores image data in S3, records metadata in DynamoDB and provides API-based retrieval.

## Future Improvements
- Add API authentication and authorization
- Implement upload validation and size restrictions
- Add automated deployment using AWS SAM or Terraform
- Introduce CI/CD using GitHub Actions

## Author
[Madhavan Paravasthu](https://github.com/MP-MadhavanParavasthu)
