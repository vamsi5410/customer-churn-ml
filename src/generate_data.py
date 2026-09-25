from pathlib import Path
import numpy as np
import pandas as pd
from src.config import RAW_DATA_DIR, FEATURES

def generate(n=2500, seed=42):
    rng = np.random.default_rng(seed)

    tenure = rng.integers(1, 73, n)
    monthly = np.round(rng.uniform(25, 125, n), 2)
    contract = rng.choice(
        ["Month-to-month", "One year", "Two year"],
        n,
        p=[0.55, 0.25, 0.20],
    )
    internet = rng.choice(["DSL", "Fiber optic", "No"], n, p=[0.35, 0.50, 0.15])
    payment = rng.choice(
        ["Electronic check", "Bank transfer", "Credit card", "Mailed check"],
        n,
        p=[0.38, 0.28, 0.22, 0.12],
    )
    tech = rng.choice(["Yes", "No"], n, p=[0.35, 0.65])
    security = rng.choice(["Yes", "No"], n, p=[0.40, 0.60])

    total = np.round(monthly * tenure * rng.uniform(0.92, 1.08, n), 2)

    score = (
        1.5 * (contract == "Month-to-month")
        + 0.8 * (internet == "Fiber optic")
        + 0.6 * (payment == "Electronic check")
        + 0.7 * (tech == "No")
        + 0.5 * (security == "No")
        + 0.8 * (tenure < 12)
        + 0.5 * (monthly > 90)
        - 0.8 * (contract == "Two year")
        - 0.5 * (tenure > 36)
        + rng.normal(0, 0.7, n)
    )
    probability = 1 / (1 + np.exp(-(score - 2.3)))
    churn = (rng.random(n) < probability).astype(int)

    df = pd.DataFrame({
        "customer_id": [f"C{10001+i}" for i in range(n)],
        "name": [f"Customer {10001+i}" for i in range(n)],
        "email": [f"customer{10001+i}@example.com" for i in range(n)],
        "phone": [f"+91-90000{10000+i:05d}" for i in range(n)],
        "tenure": tenure,
        "monthly_charges": monthly,
        "total_charges": total,
        "contract": contract,
        "internet_service": internet,
        "payment_method": payment,
        "tech_support": tech,
        "online_security": security,
        "churn": churn,
    })

    return df

if __name__ == "__main__":
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = generate()
    path = RAW_DATA_DIR / "customers.csv"
    df.to_csv(path, index=False)
    print(f"Generated {len(df)} rows -> {path}")
