import json
import logging
import time
from contextlib import asynccontextmanager

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request

from src.api.model_loader import METADATA_PATH, MODEL_PATH
from src.api.schemas import (
    HealthResponse,
    ModelInfoResponse,
    PredictionResponse,
    UserData,
)
from src.features import create_features


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model artifacts once when the API starts."""
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model artifact not found: {MODEL_PATH}")

    if not METADATA_PATH.exists():
        raise RuntimeError(f"Model metadata not found: {METADATA_PATH}")

    logger.info("Loading model and metadata")

    app.state.model = joblib.load(MODEL_PATH)

    with METADATA_PATH.open("r", encoding="utf-8") as file:
        app.state.model_info = json.load(file)

    app.state.threshold = float(app.state.model_info["threshold"])
    app.state.feature_columns = app.state.model_info["feature_columns"]

    logger.info(
        "Model loaded successfully: type=%s, threshold=%.6f",
        app.state.model_info.get("model_type", "unknown"),
        app.state.threshold,
    )

    yield

    logger.info("Shutting down API")
    app.state.model = None
    app.state.model_info = None


app = FastAPI(
    title="Credit Risk Scoring API",
    description="API for predicting loan default risk.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["General"])
def root():
    return {
        "message": "Credit Risk Scoring API is running",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
def health(request: Request):
    model_info = getattr(request.app.state, "model_info", None)
    model = getattr(request.app.state, "model", None)

    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "model_type": (
            model_info.get("model_type", "unknown")
            if model_info
            else "unknown"
        ),
        "model_created_at": (
            model_info.get("created_at", "unknown")
            if model_info
            else "unknown"
        ),
    }


@app.get(
    "/model-info",
    response_model=ModelInfoResponse,
    tags=["Model"],
)
def get_model_info(request: Request):
    model_info = getattr(request.app.state, "model_info", None)

    if model_info is None:
        raise HTTPException(
            status_code=503,
            detail="Model metadata is not loaded.",
        )

    return model_info


@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Prediction"],
)
def predict(user_data: UserData, request: Request):
    start_time = time.perf_counter()

    model = getattr(request.app.state, "model", None)
    threshold = getattr(request.app.state, "threshold", None)
    feature_columns = getattr(
        request.app.state,
        "feature_columns",
        None,
    )

    if model is None or threshold is None or feature_columns is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not ready.",
        )

    try:
        raw_df = pd.DataFrame([user_data.model_dump()])
        engineered_df = create_features(raw_df)
        model_input = engineered_df[feature_columns]

        probability = float(model.predict_proba(model_input)[0, 1])
        prediction = int(probability >= threshold)

        elapsed_time = time.perf_counter() - start_time
        logger.info(
            "Prediction completed: label=%s, latency=%.4fs",
            prediction,
            elapsed_time,
        )

        return {
            "probability": probability,
            "prediction": prediction,
            "label": "high_risk" if prediction == 1 else "low_risk",
            "threshold": threshold,
            "decision": (
                "manual_review"
                if prediction == 1
                else "approve"
            ),
        }

    except HTTPException:
        raise
    except Exception:
        elapsed_time = time.perf_counter() - start_time
        logger.exception(
            "Prediction failed after %.4fs",
            elapsed_time,
        )
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Please try again later.",
        )
