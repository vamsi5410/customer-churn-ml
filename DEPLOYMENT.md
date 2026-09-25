# ChurnAI Deployment Guide

## Render — FastAPI

Build command:
```bash
pip install -r requirements.txt && python -m src.generate_data && python -m src.train
```

Start command:
```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

## Streamlit Community Cloud

Deploy `dashboard/app.py` and set the secret:

```toml
API_URL = "https://YOUR-API.onrender.com"
```

## Docker

```bash
docker compose up --build
```

## Production AWS evolution

Use:
- Cognito for authentication
- ECS/Fargate for API containers
- RDS PostgreSQL for customer data
- S3 for uploaded files/reports
- CloudWatch for logs and monitoring

Never commit `.env`, passwords, database credentials, API keys, AWS keys, or Streamlit secrets.
