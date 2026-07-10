from typing import Literal
from pydantic import BaseModel, Field,  field_validator
import re

class UserData(BaseModel):
    loan_amnt: float = Field(..., gt=0, description="Loan amount in dollars")
    term: Literal["36 months", "60 months"] = Field(..., description="36 months or 60 months")
    emp_length: str = Field(..., description="Employment length category")
    home_ownership: str = Field(..., description="Housing status")
    annual_inc: float = Field(..., ge=0, description="Annual income in dollars")
    purpose: str = Field(..., description="Loan purpose")
    dti: float = Field(..., ge=0, description="Debt-to-income ratio")
    delinq_2yrs: int = Field(..., ge=0, description="Delinquencies in last 2 years")
    inq_last_6mths: int = Field(..., ge=0, description="Credit inquiries in last 6 months")
    open_acc: int = Field(..., ge=0, description="Number of open accounts")
    pub_rec: int = Field(..., ge=0, description="Public records count")
    revol_bal: float = Field(..., ge=0, description="Revolving balance in dollars")
    revol_util: float = Field(..., ge=0, description="Revolving utilization rate")
    total_acc: int = Field(..., ge=0, description="Total number of credit accounts")
    earliest_cr_line: str = Field(..., description="First credit line date (MMM-YYYY)")
    issue_d: str = Field(..., description="Loan issuance date (MMM-YYYY)")

    @field_validator("earliest_cr_line", "issue_d")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        if not re.fullmatch(r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4}$", v):
            raise ValueError("Date must be in MMM-YYYY format, e.g. Jan-2015")
        return v

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
    model_loaded: bool
    model_type: str
    model_created_at: str

