import json
import joblib
from pathlib import Path

def save_artifacts(
        pipeline, 
        model_info: dict,
        model_path: str = "artifacts/credit_risk_pipeline.joblib",
        info_path: str = "artifacts/model_info.json",
):
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)

    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(model_info, f, indent=4, ensure_ascii=False)

def load_artifacts(
    model_path: str = "artifacts/credit_risk_pipeline.joblib",
    info_path: str = "artifacts/model_info.json",
):
    pipeline = joblib.load(model_path)

    with open(info_path, "r", encoding="utf-8") as f:
        model_info = json.load(f)

    return pipeline, model_info 