from src.data import load_modeling_data
from src.features import create_features
from src.split import time_based_split, create_xy
from src.models import build_model_pipeline
from src.config import load_config
from src.evaluation import evaluate_at_threshold
from src.artifacts import save_artifacts
from datetime import datetime, timezone

def train(config):
    table_name=config["data"]["table_name"]
    df= load_modeling_data(table_name)
    df= create_features(df)

    train_df, val_df, test_df=  time_based_split(
        df=df,
        validation_start=config["split"]["validation_start"],
        test_start=config["split"]["test_start"],
    )

    target_column = config["data"]["target_column"]
    X_train, y_train = create_xy(
        train_df,
        target_column=target_column,
    )

    X_val, y_val = create_xy(
        val_df,
        target_column=target_column,
    )

    X_test, y_test = create_xy(
        test_df,
        target_column=target_column,
    )
    model_config = config["model"]

    pipeline = build_model_pipeline(
        X_train=X_train,
        model_type=model_config["type"],
        params=model_config["params"],
    )

    pipeline.fit(X_train, y_train)

    return (
    pipeline,
    X_train,
    X_val,
    y_val,  
    X_test,
    y_test,
)

if __name__ == "__main__":
    config = load_config("configs/config.yaml")
    pipeline, X_train, X_val, y_val, X_test, y_test = train(config)

    threshold= config["decision"]["threshold"]
    review_cost_per_application= config["business"]["review_cost"]
    default_loss_rate=config["business"]["default_loss_rate"]
    review_effectiveness=config["business"]["review_effectiveness"]

    y_proba_v=pipeline.predict_proba(X_val)[:,1]
    validation_metrics = evaluate_at_threshold(
        X=X_val,
        y_true=y_val,
        y_proba=y_proba_v,
        threshold=threshold ,
        review_cost_per_application= review_cost_per_application,
        default_loss_rate=default_loss_rate,
        review_effectiveness=review_effectiveness,
    )
    y_proba_t=pipeline.predict_proba(X_test)[:,1]

    test_metrics = evaluate_at_threshold(
        X=X_test,
        y_true=y_test,
        y_proba=y_proba_t,
        threshold=threshold ,
        review_cost_per_application= review_cost_per_application,
        default_loss_rate=default_loss_rate,
        review_effectiveness=review_effectiveness,
    )
    print(test_metrics)

    model_info = {
    "model_type": config["model"]["type"],
    "model_params": config["model"]["params"],
    "threshold": config["decision"]["threshold"],
    "review_capacity": config["decision"]["review_capacity"],
    "business_assumptions": config["business"],
    "validation_metrics": validation_metrics,
    "test_metrics": test_metrics,
    "feature_columns": list(X_train.columns),
    "split": config["split"],
    "positive_action": config["decision"]["positive_action"],
    "negative_action": config["decision"]["negative_action"],
    "created_at": datetime.now(timezone.utc).isoformat(),
    }
    model_path = config["artifacts"]["model_path"]
    info_path = config["artifacts"]["model_info_path"]
    save_artifacts(pipeline, model_info, model_path, info_path)


