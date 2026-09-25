from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT_DIR / "models"
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
REPORT_DIR = ROOT_DIR / "reports"

MODEL_PATH = Path(os.getenv("MODEL_PATH", str(MODEL_DIR / "model.joblib")))
PREPROCESSOR_PATH = Path(os.getenv("PREPROCESSOR_PATH", str(MODEL_DIR / "preprocessor.joblib")))
METADATA_PATH = Path(os.getenv("METADATA_PATH", str(MODEL_DIR / "metadata.json")))

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{ROOT_DIR / 'churnai.db'}")

FEATURES = [
    "tenure",
    "monthly_charges",
    "total_charges",
    "contract",
    "internet_service",
    "payment_method",
    "tech_support",
    "online_security",
]

CATEGORICAL_FEATURES = [
    "contract",
    "internet_service",
    "payment_method",
    "tech_support",
    "online_security",
]

NUMERIC_FEATURES = [
    "tenure",
    "monthly_charges",
    "total_charges",
]
