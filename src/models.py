from sklearn.pipeline import Pipeline

def build_model_pipeline(preprocessor, model):
    pipeline = Pipeline([           # ← pipeline (строчная)
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    return pipeline
