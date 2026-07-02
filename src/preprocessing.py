from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def create_preprocessor(X_train):
    num_columns= X_train.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()
    cat_columns=X_train.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    num_transform= Pipeline(
        [('imputer',  SimpleImputer(strategy="median")),
         ('scaler', StandardScaler())]
        )
    cat_transform= Pipeline(
        [('imputer', SimpleImputer(strategy='most_frequent')),
         ('onehot', OneHotEncoder(
            handle_unknown= 'ignore',
         ) )]
    )

    preprocessor= ColumnTransformer(
        [
            ('num', num_transform, num_columns),
            ('cat', cat_transform,cat_columns)
        ]
    )
    return preprocessor