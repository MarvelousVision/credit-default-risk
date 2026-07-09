from fastapi import FastAPI, HTTPException
from src.api.schemas import UserData, ModelInfoResponse, PredictionResponse, HealthResponse
from src.api.model_loader import model, model_info, THRESHOLD
import pandas as pd
from src.features import create_features
from src.split import FEATURE_COLUMNS

app = FastAPI(title="Loan Default Prediction")

@app.get("/health", response_model=HealthResponse)
def health():
    return {
  "status": "ok",
  "model_loaded": True
}

@app.get('/model-info', response_model=ModelInfoResponse)
def get_model_info():
    return model_info

@app.post("/predict",response_model=PredictionResponse)
def predict(user_data: UserData):
    try:
        data= user_data.model_dump()
        df= pd.DataFrame([data])
        engineered_df = create_features(df)
        X = engineered_df[FEATURE_COLUMNS]
        
        probability = model.predict_proba(X)[0, 1]
        prediction = int(probability >= THRESHOLD)
        
        return {
            "probability": float(probability),
            "prediction": prediction,
            "label": "high_risk" if prediction == 1 else "low_risk",
            "threshold": THRESHOLD,
            "decision": "manual_review" if prediction == 1 else "approve"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
def root():
    return {"message": "Credit Risk Scoring API is running", "docs": "/docs"}    
