from typing import Optional
import io
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.database import init_db, get_db, Customer, Prediction
from src.ml import get_model, predict_one, model_metadata
from src.config import FEATURES

app = FastAPI(
    title="ChurnAI API",
    version="1.0.0",
    description="Cloud-ready customer churn intelligence platform",
)

init_db()

class CustomerInput(BaseModel):
    customer_id: str = Field(min_length=1, max_length=80)
    name: str = ""
    email: str = ""
    phone: str = ""
    tenure: int = Field(ge=0, le=120)
    monthly_charges: float = Field(ge=0)
    total_charges: float = Field(ge=0)
    contract: str
    internet_service: str
    payment_method: str
    tech_support: str
    online_security: str

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tenure: Optional[int] = Field(default=None, ge=0, le=120)
    monthly_charges: Optional[float] = Field(default=None, ge=0)
    total_charges: Optional[float] = Field(default=None, ge=0)
    contract: Optional[str] = None
    internet_service: Optional[str] = None
    payment_method: Optional[str] = None
    tech_support: Optional[str] = None
    online_security: Optional[str] = None

def customer_dict(c: Customer):
    return {
        "customer_id": c.customer_id,
        "name": c.name,
        "email": c.email,
        "phone": c.phone,
        "tenure": c.tenure,
        "monthly_charges": c.monthly_charges,
        "total_charges": c.total_charges,
        "contract": c.contract,
        "internet_service": c.internet_service,
        "payment_method": c.payment_method,
        "tech_support": c.tech_support,
        "online_security": c.online_security,
        "churn_probability": c.churn_probability,
        "risk_level": c.risk_level,
        "recommendation": c.recommendation,
    }

@app.get("/")
def root():
    return {"service": "ChurnAI", "version": "1.0.0"}

@app.get("/health")
def health():
    try:
        get_model()
        return {"status": "ok", "model_ready": True}
    except Exception as exc:
        return {"status": "degraded", "model_ready": False, "error": str(exc)}

@app.get("/model/info")
def model_info():
    return model_metadata()

@app.get("/customers")
def list_customers(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    rows = db.query(Customer).offset(offset).limit(min(limit, 1000)).all()
    return [customer_dict(row) for row in rows]

@app.get("/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_dict(customer)

@app.post("/customers")
def create_customer(payload: CustomerInput, db: Session = Depends(get_db)):
    if db.get(Customer, payload.customer_id):
        raise HTTPException(status_code=409, detail="Customer already exists")

    customer = Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer_dict(customer)

@app.put("/customers/{customer_id}")
def update_customer(customer_id: str, payload: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer_dict(customer)

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"deleted": customer_id}

@app.post("/predict")
def predict(payload: CustomerInput, db: Session = Depends(get_db)):
    result = predict_one(payload.model_dump())

    customer = db.get(Customer, payload.customer_id)
    if customer:
        customer.churn_probability = result["churn_probability"]
        customer.risk_level = result["risk_level"]
        customer.recommendation = result["recommendation"]
    else:
        customer = Customer(**payload.model_dump())
        customer.churn_probability = result["churn_probability"]
        customer.risk_level = result["risk_level"]
        customer.recommendation = result["recommendation"]
        db.add(customer)

    db.add(Prediction(
        customer_id=payload.customer_id,
        churn_probability=result["churn_probability"],
        risk_level=result["risk_level"],
        recommendation=result["recommendation"],
    ))
    db.commit()

    return result

@app.post("/predict/bulk")
async def predict_bulk(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file")

    raw = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(raw))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {exc}")

    required = ["customer_id"] + FEATURES
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail={"missing_columns": missing})

    records = df[required].to_dict(orient="records")
    results = []

    for record in records:
        try:
            result = predict_one(record)
            results.append(result)

            customer = db.get(Customer, str(record["customer_id"]))
            if customer:
                customer.churn_probability = result["churn_probability"]
                customer.risk_level = result["risk_level"]
                customer.recommendation = result["recommendation"]
            else:
                customer = Customer(
                    customer_id=str(record["customer_id"]),
                    name=str(record.get("name", "")),
                    email=str(record.get("email", "")),
                    phone=str(record.get("phone", "")),
                    tenure=int(record["tenure"]),
                    monthly_charges=float(record["monthly_charges"]),
                    total_charges=float(record["total_charges"]),
                    contract=str(record["contract"]),
                    internet_service=str(record["internet_service"]),
                    payment_method=str(record["payment_method"]),
                    tech_support=str(record["tech_support"]),
                    online_security=str(record["online_security"]),
                    churn_probability=result["churn_probability"],
                    risk_level=result["risk_level"],
                    recommendation=result["recommendation"],
                )
                db.add(customer)

            db.add(Prediction(
                customer_id=str(record["customer_id"]),
                churn_probability=result["churn_probability"],
                risk_level=result["risk_level"],
                recommendation=result["recommendation"],
            ))
        except Exception as exc:
            results.append({
                "customer_id": str(record.get("customer_id", "")),
                "error": str(exc),
            })

    db.commit()
    return {
        "processed": len(results),
        "high_risk": sum(r.get("risk_level") == "HIGH" for r in results),
        "medium_risk": sum(r.get("risk_level") == "MEDIUM" for r in results),
        "low_risk": sum(r.get("risk_level") == "LOW" for r in results),
        "results": results,
    }

@app.get("/predictions")
def predictions(limit: int = 100, db: Session = Depends(get_db)):
    rows = (
        db.query(Prediction)
        .order_by(Prediction.created_at.desc())
        .limit(min(limit, 1000))
        .all()
    )
    return [
        {
            "id": r.id,
            "customer_id": r.customer_id,
            "churn_probability": r.churn_probability,
            "risk_level": r.risk_level,
            "recommendation": r.recommendation,
            "created_at": r.created_at.isoformat(),
        }
        for r in rows
    ]

@app.get("/analytics/summary")
def analytics_summary(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    total = len(customers)

    high = sum(c.risk_level == "HIGH" for c in customers)
    medium = sum(c.risk_level == "MEDIUM" for c in customers)
    low = sum(c.risk_level == "LOW" for c in customers)
    scored = [c for c in customers if c.churn_probability is not None]

    avg_probability = (
        sum(c.churn_probability for c in scored) / len(scored)
        if scored else 0
    )
    revenue_at_risk = sum(
        c.monthly_charges for c in scored if c.churn_probability and c.churn_probability >= 0.5
    )

    return {
        "total_customers": total,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "scored_customers": len(scored),
        "average_churn_probability": round(avg_probability, 4),
        "monthly_revenue_at_risk": round(revenue_at_risk, 2),
    }
