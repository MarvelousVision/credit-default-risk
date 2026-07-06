import pandas as pd

def time_based_split(
    df: pd.DataFrame,
    validation_start: str,
    test_start: str,
    date_column: str = "issue_date",
):
    df_sorted = df.sort_values(date_column).reset_index(drop=True)

    validation_start = pd.Timestamp(validation_start)
    test_start = pd.Timestamp(test_start)

    train_df = df_sorted[
        df_sorted[date_column] < validation_start
    ]

    val_df = df_sorted[
        (df_sorted[date_column] >= validation_start)
        & (df_sorted[date_column] < test_start)
    ]

    test_df = df_sorted[
        df_sorted[date_column] >= test_start
    ]

    return train_df, val_df, test_df

FEATURE_COLUMNS = [
    "loan_amnt",
    "home_ownership",
    "purpose",
    "dti",
    "delinq_2yrs",
    "inq_last_6mths",
    "open_acc",
    "pub_rec",
    "revol_bal",
    "revol_util",
    "total_acc",
    "term_months",
    "emp_length_years",
    "annual_inc_log",
    "credit_history_length_years",
]


def create_xy(
    df: pd.DataFrame,
    target_column: str,
):
    X = df[FEATURE_COLUMNS].copy()
    y = df[target_column].copy()

    return X, y


