import json
import joblib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT_DIR / "src"

MODEL_PATH = ROOT_DIR / "artifacts" / "credit_risk_pipeline.joblib"
METADATA_PATH = ROOT_DIR / "artifacts" / "model_info.json"
    