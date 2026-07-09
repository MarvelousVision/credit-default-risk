from pydantic import BaseModel

class UserData(BaseModel):
    loan_amnt: float
    term: str                  
    emp_length: str            
    home_ownership: str        
    annual_inc: float
    purpose: str               
    dti: float
    delinq_2yrs: int
    earliest_cr_line: str      
    inq_last_6mths: int
    open_acc: int
    pub_rec: int
    revol_bal: float
    revol_util: float
    total_acc: int
    issue_d: str

class PredictionResponse(BaseModel):
    probability: float
    prediction: int
    label: str
    threshold: float
    decision: str 

class ModelInfoResponse(BaseModel):
    model_type: str
    model_params: dict
    threshold: float
    review_capacity: float
    positive_action: str
    negative_action: str
    business_assumptions: dict
    validation_metrics: dict
    test_metrics: dict
    feature_columns: list
    split: dict
    created_at: str

class HealthResponse(BaseModel):
    status: str

