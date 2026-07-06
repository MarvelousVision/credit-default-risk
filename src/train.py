from src.data import load_modeling_data
from src.features import create_features
from src.split import time_based_split, create_xy
from src.models import build_model_pipeline
from src.config import load_config
from src.evaluation import evaluate_at_threshold

def train(config_path: str = "configs/config.yaml"):
    config = load_config(config_path)
    table_name=config["data"]["table_name"]
    df= load_modeling_data(table_name)
    df= create_features(df)

    threshold= config["decision"]["threshold"]
    review_cost_per_application= config["business"]["review_cost"]
    default_loss_rate=config["business"]["default_loss_rate"]
    review_effectiveness=config["business"]["review_effectiveness"]

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
    X_val,
    y_val,
    X_test,
    y_test,
    threshold,
    review_cost_per_application,
    default_loss_rate,
    review_effectiveness,
)

if __name__ == "__main__":
    model, X_val, y_val, X_test, y_test, threshold, review_cost_per_application ,default_loss_rate , review_effectiveness = train()
    y_proba=model.predict_proba(X_val)[:,1]

    validation_metrics = evaluate_at_threshold(
        X=X_val,
        y_true=y_val,
        y_proba=y_proba,
        threshold=threshold ,
        review_cost_per_application= review_cost_per_application,
        default_loss_rate=default_loss_rate,
        review_effectiveness=review_effectiveness,
    )
    print(validation_metrics)
