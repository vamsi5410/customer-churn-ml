
# ChurnAI — Customer Churn Prediction Platform

ChurnAI is an end-to-end machine learning application for predicting customer churn and identifying customers at different risk levels.

The project combines a machine learning model with a FastAPI backend, Streamlit dashboard, SQL database, automated testing, and Docker support.

---

## Overview

Customer churn is an important business problem where customers stop using a company's products or services.

ChurnAI uses customer information to estimate the probability of churn and provides a risk classification that can be used to support customer retention decisions.

The application is designed as a complete machine learning workflow:

```text
Data
  ↓
Preprocessing
  ↓
Model Training
  ↓
Model Evaluation
  ↓
Model Serialization
  ↓
FastAPI
  ↓
Streamlit Dashboard
  ↓
Prediction & Analytics
````

---

## Key Features

* Customer churn prediction
* Churn probability estimation
* Customer risk classification
* Retention recommendations
* Individual customer prediction
* Bulk customer prediction
* Customer management
* Prediction history
* Customer analytics
* Model information
* REST API
* Interactive web dashboard
* SQL database integration
* Docker support
* Automated testing
* GitHub Actions CI

---

## Technology Stack

| Technology     | Purpose                 |
| -------------- | ----------------------- |
| Python         | Application development |
| Pandas         | Data processing         |
| NumPy          | Numerical operations    |
| Scikit-learn   | Machine learning        |
| Random Forest  | Churn classification    |
| Joblib         | Model serialization     |
| FastAPI        | Backend REST API        |
| Pydantic       | API validation          |
| Streamlit      | Web dashboard           |
| SQL            | Database                |
| Pytest         | Automated testing       |
| Docker         | Containerization        |
| GitHub Actions | Continuous integration  |

---

# Machine Learning

## Model

ChurnAI uses a **Random Forest Classifier** for customer churn prediction.

The model is configured with:

```python
RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_leaf=3,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
```

The model uses a preprocessing pipeline before classification.

---

## Preprocessing

### Numerical Features

The following numerical features are used:

* `tenure`
* `monthly_charges`
* `total_charges`

Numerical preprocessing includes:

* Missing-value imputation
* Feature scaling

### Categorical Features

The following categorical features are used:

* `contract`
* `internet_service`
* `payment_method`
* `tech_support`
* `online_security`

Categorical preprocessing includes:

* Missing-value imputation
* One-hot encoding

---

## Model Pipeline

```text
Customer Dataset
       │
       ▼
Train/Test Split
       │
       ▼
Missing Value Handling
       │
       ▼
Numerical Scaling
       │
       ▼
Categorical Encoding
       │
       ▼
Random Forest Classifier
       │
       ▼
Model Evaluation
       │
       ▼
Model Serialization
```

The preprocessing objects and trained model are stored as serialized artifacts for API inference.

---

# Application Dashboard

The Streamlit dashboard provides multiple sections for working with customer churn predictions.

## 1. Executive Dashboard

Provides an overview of customer and prediction analytics.

The dashboard can display information such as:

* Customer statistics
* Churn statistics
* Risk distribution
* Prediction analytics

---

## 2. Customer Prediction

Allows a user to enter customer information and generate an individual churn prediction.

The prediction workflow is:

```text
Customer Information
        ↓
FastAPI
        ↓
Preprocessing
        ↓
ML Model
        ↓
Churn Probability
        ↓
Risk Level
        ↓
Recommendation
```

The result includes:

* Prediction
* Churn probability
* Risk level
* Retention recommendation

---

## 3. Customer Management

Provides access to customer information through the backend API.

Users can retrieve customer records and use them for prediction and analysis.

---

## 4. Bulk Prediction

Allows multiple customer records to be processed together.

```text
Customer Dataset
       ↓
Bulk Prediction API
       ↓
ML Model
       ↓
Predictions
       ↓
Results
```

This is useful when predictions need to be generated for multiple customers instead of processing them individually.

---

## 5. Prediction History

Stores and displays previous prediction results.

This allows prediction activity to be reviewed after predictions have been generated.

---

## 6. Model Information

Provides information about the deployed machine learning model and its training metadata.

---

# FastAPI Backend

ChurnAI uses FastAPI as the backend service.

The backend is responsible for:

* Request validation
* Customer data processing
* Model inference
* Prediction generation
* Customer management
* Prediction history
* Analytics
* Model information

---

## API Endpoints

| Method | Endpoint             | Description                    |
| ------ | -------------------- | ------------------------------ |
| `GET`  | `/`                  | API information                |
| `GET`  | `/health`            | API health check               |
| `POST` | `/predict`           | Predict churn for one customer |
| `GET`  | `/customers`         | Retrieve customers             |
| `POST` | `/predict/bulk`      | Generate bulk predictions      |
| `GET`  | `/predictions`       | Retrieve prediction history    |
| `GET`  | `/analytics/summary` | Retrieve analytics summary     |
| `GET`  | `/model/info`        | Retrieve model information     |

---

# API Documentation

FastAPI automatically provides interactive API documentation.

When running locally:

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# Database

The application uses SQL-based storage for application data.

The database is used for information such as:

* Customer records
* Prediction results
* Prediction history
* Analytics data

The database schema is available in:

```text
sql/schema.sql
```

For production deployment, a persistent managed database should be used instead of relying on a local database file.

---

# Project Structure

```text
customer-churn-ml/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── Dockerfile
├── docker-compose.yml
│
├── api/
│   ├── __init__.py
│   └── main.py
│
├── dashboard/
│   └── app.py
│
├── src/
│   ├── __init__.py
│   ├── generate_data.py
│   └── train.py
│
├── models/
│   ├── model.joblib
│   ├── preprocessor.joblib
│   └── metadata.json
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   └── metrics.json
│
├── sql/
│   └── schema.sql
│
├── tests/
│   ├── test_model.py
│   └── test_api.py
│
├── docs/
│   └── architecture.md
│
└── .github/
    └── workflows/
        └── ci.yml
```

---

# Local Setup

## Requirements

Install:

* Python 3.10+
* Git
* Optional: Docker

---

## 1. Clone the Repository

```bash
git clone https://github.com/vamsi5410/customer-churn-ml.git
```

Move into the project:

```bash
cd customer-churn-ml
```

---

## 2. Create Virtual Environment

### Windows

```cmd
python -m venv .venv
```

Activate:

```cmd
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Generate Dataset

The project contains a data generation script.

Run:

```bash
python src/generate_data.py
```

This generates the dataset required for model training.

---

# Train the Model

Run:

```bash
python src/train.py
```

The training pipeline:

1. Loads the dataset
2. Splits the data into training and testing sets
3. Preprocesses numerical features
4. Encodes categorical features
5. Trains the Random Forest model
6. Evaluates the model
7. Saves the trained model
8. Saves preprocessing artifacts
9. Saves model metadata
10. Saves evaluation metrics

Generated artifacts are stored in:

```text
models/
```

Evaluation information is stored in:

```text
reports/
```

---

# Run the FastAPI Backend

From the project root:

```bash
uvicorn api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# Run the Streamlit Dashboard

Open another terminal.

Activate the virtual environment if necessary:

```cmd
.venv\Scripts\activate
```

Then run:

```bash
streamlit run dashboard/app.py
```

The dashboard will normally be available at:

```text
http://localhost:8501
```

---

# API Configuration

The Streamlit dashboard communicates with the FastAPI backend using the `API_URL` configuration.

For local development:

```text
http://127.0.0.1:8000
```

For deployment:

```text
https://your-api-url.onrender.com
```

The application can use an environment variable:

```text
API_URL
```

Example:

```text
API_URL=https://your-api-url.onrender.com
```

---

# Testing

The project uses Pytest for automated testing.

Run:

```bash
pytest
```

For detailed output:

```bash
pytest -v
```

The test suite includes tests for:

* Machine learning functionality
* API functionality

---

# Docker

## Build Docker Image

```bash
docker build -t churnai .
```

## Run Docker Container

```bash
docker run -p 8000:8000 churnai
```

The FastAPI service can then be accessed at:

```text
http://localhost:8000
```

---

# Docker Compose

If using Docker Compose:

```bash
docker compose up --build
```

To stop the services:

```bash
docker compose down
```

---

# Deployment

The application can be deployed using separate frontend and backend services.

```text
                 GitHub
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
   Streamlit Cloud          Render
      Frontend              Backend
          │                   │
          └─────────┬─────────┘
                    │
                    ▼
              ML Application
                    │
                    ▼
                Database
```

## Streamlit Community Cloud

Use the Streamlit dashboard entry point:

```text
dashboard/app.py
```

Configure the backend URL using:

```text
API_URL
```

---

## Render

FastAPI can be deployed as a web service.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

After deployment, the backend URL can be used as the Streamlit `API_URL`.

---

# Environment Variables

Do not commit sensitive information to GitHub.

Recommended ignored files:

```text
.env
.streamlit/secrets.toml
*.db
.venv/
__pycache__/
```

Never commit:

* Passwords
* API keys
* Database credentials
* Access tokens
* Private secrets

---

# Example Customer

Example input:

```json
{
  "tenure": 4,
  "monthly_charges": 109.0,
  "total_charges": 436.0,
  "contract": "Month-to-month",
  "internet_service": "Fiber optic",
  "payment_method": "Electronic check",
  "tech_support": "No",
  "online_security": "No"
}
```

The API processes the customer through the trained preprocessing and classification pipeline and returns the prediction information.

---

# Model Artifacts

The trained model produces artifacts such as:

```text
models/
├── model.joblib
├── preprocessor.joblib
└── metadata.json
```

Evaluation results:

```text
reports/
└── metrics.json
```

---

# Security Considerations

This project is intended as a machine learning application and demonstration project.

For production deployment, additional security controls should be considered, including:

* Authentication
* Authorization
* HTTPS
* Input validation
* Rate limiting
* Secure database credentials
* Secret management
* API monitoring
* Logging
* Database access controls

---

# Future Improvements

Possible future improvements include:

* PostgreSQL production database
* User authentication
* Role-based access control
* SHAP model explanations
* Feature importance visualization
* Model monitoring
* Model drift detection
* Automated retraining
* Customer segmentation
* Advanced retention recommendations
* Cloud monitoring
* CI/CD deployment
* Model versioning

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

# Author

**Vamsi Krishna**

GitHub:

[https://github.com/vamsi5410](https://github.com/vamsi5410)

Repository:

[https://github.com/vamsi5410/customer-churn-ml](https://github.com/vamsi5410/customer-churn-ml)

---

## Project Summary

**ChurnAI** demonstrates an end-to-end machine learning workflow:

```text
Data Generation
      ↓
Machine Learning
      ↓
Model Evaluation
      ↓
FastAPI
      ↓
SQL Database
      ↓
Streamlit Dashboard
      ↓
Docker
      ↓
Cloud Deployment
```

Built with **Python, Scikit-learn, FastAPI, Streamlit, SQL, Docker, and GitHub Actions**.

````

### Then save and push

```cmd
cd C:\Users\Vamsi\Downloads\churnai_full_project
notepad README.md
````

Paste the entire README above → **Ctrl+S** → close Notepad.

Then:

```cmd
git add README.md
git commit -m "Update professional README"
git push origin main
```


