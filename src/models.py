from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from src.preprocessing import create_preprocessor


MODEL_REGISTRY = {
    "logistic_regression": LogisticRegression,
    "random_forest": RandomForestClassifier,
    "lightgbm": LGBMClassifier,
}


def build_model(model_type: str, params: dict):
    if model_type not in MODEL_REGISTRY:
        available = ", ".join(MODEL_REGISTRY)
        raise ValueError(
            f"Unknown model type: {model_type}. "
            f"Available models: {available}"
        )

    model_class = MODEL_REGISTRY[model_type]
    return model_class(**params)


def build_model_pipeline(X_train, model_type: str, params: dict):
    preprocessor = create_preprocessor(X_train)
    model = build_model(model_type, params)

    return Pipeline([
        ("prep", preprocessor),
        ("model", model),
    ])