from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from src.api.app import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


HIGH_RISK_PAYLOAD = {
    "loan_amnt": 18000,
    "term": "60 months",
    "emp_length": "3 years",
    "home_ownership": "RENT",
    "annual_inc": 42000,
    "purpose": "debt_consolidation",
    "dti": 34.5,
    "delinq_2yrs": 2,
    "earliest_cr_line": "Jan-2010",
    "inq_last_6mths": 4,
    "open_acc": 9,
    "pub_rec": 1,
    "revol_bal": 16000,
    "revol_util": 88.5,
    "total_acc": 18,
    "issue_d": "Dec-2018",
}


LOW_RISK_PAYLOAD = {
    "loan_amnt": 5000,
    "term": "36 months",
    "emp_length": "10+ years",
    "home_ownership": "MORTGAGE",
    "annual_inc": 95000,
    "purpose": "credit_card",
    "dti": 8.5,
    "delinq_2yrs": 0,
    "earliest_cr_line": "May-2002",
    "inq_last_6mths": 0,
    "open_acc": 12,
    "pub_rec": 0,
    "revol_bal": 3500,
    "revol_util": 18.0,
    "total_acc": 30,
    "issue_d": "Dec-2018",
}


def test_health_returns_200(client):
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"ok", "healthy"}


def test_model_info_returns_frozen_threshold(client):
    response = client.get("/model-info")

    assert response.status_code == 200
    body = response.json()

    assert body["model_type"] == "lightgbm"
    assert body["threshold"] == 0.2574331564883078
    assert body["positive_action"] == "manual_review"
    assert body["negative_action"] == "approve"


def test_high_risk_application_goes_to_manual_review(client):
    response = client.post("/predict", json=HIGH_RISK_PAYLOAD)

    assert response.status_code == 200
    body = response.json()

    assert body["prediction"] == 1
    assert body["label"] == "high_risk"
    assert body["decision"] == "manual_review"
    assert body["probability"] >= body["threshold"]


def test_low_risk_application_is_approved(client):
    response = client.post("/predict", json=LOW_RISK_PAYLOAD)

    assert response.status_code == 200
    body = response.json()

    assert body["prediction"] == 0
    assert body["label"] == "low_risk"
    assert body["decision"] == "approve"
    assert body["probability"] < body["threshold"]


def test_unseen_purpose_still_returns_prediction(client):
    payload = deepcopy(LOW_RISK_PAYLOAD)
    payload["purpose"] = "wedding_expenses"

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["decision"] in {"approve", "manual_review"}


def test_missing_required_field_returns_422(client):
    payload = deepcopy(LOW_RISK_PAYLOAD)
    payload.pop("loan_amnt")

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_negative_loan_amount_returns_422(client):
    payload = deepcopy(LOW_RISK_PAYLOAD)
    payload["loan_amnt"] = -1000

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_invalid_date_format_returns_422(client):
    payload = deepcopy(LOW_RISK_PAYLOAD)
    payload["issue_d"] = "2018-12-01"

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
