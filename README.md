# ChurnAI — Cloud-Based Customer Churn Intelligence Platform

An end-to-end customer churn prediction platform built with:

- Python + scikit-learn
- FastAPI REST API
- Streamlit dashboard
- PostgreSQL/SQLite database support
- Bulk CSV prediction
- Customer CRUD
- Prediction history
- Analytics
- AI retention recommendations
- Explainable feature importance
- Docker + Docker Compose
- GitHub Actions CI
- Cloud-ready environment configuration

## Architecture

```text
Streamlit Dashboard
        |
        v
    FastAPI API
     /       \
    v         v
Database    ML Pipeline
    |          |
PostgreSQL  Random Forest
    |
Prediction History
```

## Project structure

```text
churnai/
├── api/
│   └── main.py
├── dashboard/
│   └── app.py
├── src/
│   ├── config.py
│   ├── database.py
│   ├── generate_data.py
│   ├── ml.py
│   └── train.py
├── models/
├── data/raw/
├── reports/
├── tests/
├── sql/
├── .github/workflows/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 1. Local setup

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.generate_data
python -m src.train
uvicorn api.main:app --reload
```

Open:

- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

Second terminal:

```powershell
.venv\Scripts\activate
streamlit run dashboard/app.py
```

Open:

- Dashboard: http://localhost:8501

## 2. Docker

```bash
docker compose up --build
```

Dashboard: http://localhost:8501  
API: http://localhost:8000/docs

## 3. Environment variables

Copy `.env.example` to `.env`.

Important variables:

```env
DATABASE_URL=sqlite:///./churnai.db
API_URL=http://127.0.0.1:8000
MODEL_PATH=models/model.joblib
PREPROCESSOR_PATH=models/preprocessor.joblib
```

For PostgreSQL:

```env
DATABASE_URL=postgresql+psycopg://user:password@host:5432/churnai
```

## 4. API endpoints

### Health

`GET /health`

### Customers

`GET /customers`

`POST /customers`

`GET /customers/{customer_id}`

`PUT /customers/{customer_id}`

`DELETE /customers/{customer_id}`

### Prediction

`POST /predict`

### Bulk prediction

`POST /predict/bulk`

Upload a CSV file.

### Analytics

`GET /analytics/summary`

### Prediction history

`GET /predictions`

## 5. CSV format

Required columns:

```text
customer_id
tenure
monthly_charges
total_charges
contract
internet_service
payment_method
tech_support
online_security
```

Example:

```csv
customer_id,tenure,monthly_charges,total_charges,contract,internet_service,payment_method,tech_support,online_security
C1001,4,109,436,Month-to-month,Fiber optic,Electronic check,No,No
C1002,48,55,2640,Two year,DSL,Credit card,Yes,Yes
```

## 6. Production roadmap

For a production AWS deployment, the same API can be placed behind a load balancer with PostgreSQL/RDS, S3 for files, Cognito for authentication, and CloudWatch for monitoring.

Do not commit passwords, API keys, cloud credentials, or `.env` files.
