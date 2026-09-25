# ChurnAI Architecture

## Current portfolio architecture

```text
Streamlit
   |
   v
FastAPI
   |
   +------> SQL database
   |
   +------> Random Forest model
   |
   +------> Prediction history
```

## Enterprise evolution

```text
Users
 |
 v
Authentication
 |
 v
Load Balancer
 |
 v
FastAPI services
 |             \
 v              v
PostgreSQL      ML inference
 |
 +--> object storage
 |
 +--> audit logs
```

Recommended future AWS services:

- Cognito for authentication
- ECS/Fargate for containerized API
- RDS PostgreSQL for relational data
- S3 for uploaded CSVs/reports
- CloudWatch for logs and monitoring
