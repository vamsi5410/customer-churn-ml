import json
from functools import lru_cache
from joblib import load
import pandas as pd

from src.config import MODEL_PATH, METADATA_PATH, FEATURES

@lru_cache(maxsize=1)
def get_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model not found. Run: python -m src.generate_data && python -m src.train"
        )
    return load(MODEL_PATH)

def risk_level(probability: float) -> str:
    if probability >= 0.70:
        return "HIGH"
    if probability >= 0.40:
        return "MEDIUM"
    return "LOW"

def recommendation(row: dict, probability: float) -> str:
    actions = []

    if probability >= 0.70:
        actions.append("Contact customer within 48 hours.")
    if row["contract"] == "Month-to-month":
        actions.append("Offer an annual or two-year contract incentive.")
    if row["tech_support"] == "No":
        actions.append("Offer a technical-support trial or package.")
    if row["online_security"] == "No":
        actions.append("Offer an online-security bundle.")
    if row["monthly_charges"] >= 90:
        actions.append("Review pricing and offer a suitable retention plan.")
    if row["tenure"] < 12:
        actions.append("Use an early-lifecycle onboarding offer.")

    if not actions:
        actions.append("Maintain engagement and monitor future churn signals.")

    return " ".join(actions)

def predict_one(customer: dict) -> dict:
    model = get_model()
    row = {feature: customer[feature] for feature in FEATURES}
    df = pd.DataFrame([row])
    probability = float(model.predict_proba(df)[0, 1])
    level = risk_level(probability)

    return {
        "customer_id": customer.get("customer_id", ""),
        "prediction": int(probability >= 0.5),
        "churn_probability": round(probability, 4),
        "risk_level": level,
        "recommendation": recommendation(customer, probability),
    }

def model_metadata():
    if METADATA_PATH.exists():
        return json.loads(METADATA_PATH.read_text())
    return {}
