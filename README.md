# Credit Default Risk Prediction

End-to-end machine learning project for predicting credit default risk and supporting loan application review decisions.

The project includes:

- PostgreSQL-based data preparation;
- leakage-aware feature engineering;
- time-based train/validation/test split;
- LightGBM model training;
- business threshold selection;
- model evaluation with ML and business metrics;
- error analysis;
- FastAPI inference service;
- Dockerized API deployment.

---

## Project Overview

The goal of this project is to build a machine learning system that estimates borrower default risk and converts the model score into a business decision.

The system predicts whether a loan application should be:

- approved automatically;
- sent to manual review.

This project focuses not only on model quality, but also on realistic ML engineering practices:

- clean project structure;
- reproducible training;
- saved model artifacts;
- API inference;
- automated API tests;
- Docker deployment.

---

## Business Problem

A lending company needs to reduce losses from risky borrowers while avoiding unnecessary manual review for good borrowers.

Two types of mistakes are important:

| Error Type | Meaning | Business Impact |
|---|---|---|
| False Positive | Good borrower is marked as risky | Extra manual review cost and worse customer experience |
| False Negative | Risky borrower is approved | Potential financial loss from default |

False negatives are considered more expensive because approving a borrower who defaults can create a large financial loss.
The model is used as a decision-support system, not as a fully automatic rejection tool.

---

## Data

The project uses Lending Club loan data.

The modeling table is stored in PostgreSQL:
```text
loans_modeling_v1
```

The target is binary:

| Target | Meaning |
|---|---|
| `0` | Fully paid loan |
| `1` | Charged off / defaulted loan |

The final modeling dataset contains approximately:

```text
1,303,638 rows
```

Default rate:

```text
~20.1%
```

---

## Features

The final conservative feature set excludes lender-generated and potentially leakage-prone variables.

Final model features:

```text
loan_amnt
home_ownership
purpose
dti
delinq_2yrs
inq_last_6mths
open_acc
pub_rec
revol_bal
revol_util
total_acc
term_months
emp_length_years
annual_inc_log
credit_history_length_years
```

Feature engineering includes:

- converting loan term into numeric months;
- extracting employment length as numeric years;
- log-transforming annual income;
- calculating credit history length;
- processing categorical and numerical features in a pipeline.

---

## Time-Based Split

The project uses a time-based split instead of a random split.

This better simulates production because the model is trained on past loans and evaluated on future loans.

| Split | Period |
|---|---|
| Train | Before 2016-03-01 |
| Validation | 2016-03-01 to 2016-12-31 |
| Test | 2017-01-01 onward |

The test set is used only for final evaluation.

---

## Modeling Approach

The final model is a LightGBM classifier inside an sklearn-compatible pipeline.

Model:

```text
LGBMClassifier(random_state=42, verbosity=-1)
```

Saved artifacts:

```text
artifacts/credit_risk_pipeline.joblib
artifacts/model_info.json
```

The pipeline includes preprocessing, trained model, and inference-ready transformations.

---

## Threshold Selection

The model does not use the default threshold of `0.5`.
Instead, the threshold was selected on the validation set using a manual review capacity rule.

Business rule:

```text
Flag approximately the top 20% riskiest applications for manual review.
```

Final threshold:

```text
0.2574331564883078
```

Decision logic:

```text
score >= threshold → high_risk → manual_review
score < threshold  → low_risk  → approve
```

The model score is not probability-calibrated, so it should be interpreted as a risk score rather than an exact real-world probability.

---

## Business Metric

The business metric estimates the cost of wrong decisions and manual reviews.

Business assumptions:

| Parameter | Value |
|---|---:|
| Review cost | `$100` |
| Default loss rate | `60%` of loan amount |
| Review effectiveness | `100%` |
| Manual review capacity | `20%` |

The cost function is illustrative and used to compare decision strategies.

---

## Final Results

### Validation Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.7206 |
| Precision | 0.4381 |
| Recall | 0.3441 |
| F1 | 0.3854 |
| ROC-AUC | 0.6809 |
| PR-AUC | 0.4121 |
| Flagged rate | 0.2000 |
| Total estimated cost | `$294,408,645` |

Validation confusion matrix:

|  | Predicted Low Risk | Predicted High Risk |
|---|---:|---:|
| Actual Low Risk | 135,867 | 24,124 |
| Actual Default | 35,853 | 18,806 |

### Test Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.7369 |
| Precision | 0.3694 |
| Recall | 0.3553 |
| F1 | 0.3622 |
| ROC-AUC | 0.6856 |
| PR-AUC | 0.3498 |
| Flagged rate | 0.2023 |
| Total estimated cost | `$236,546,965` |

Test confusion matrix:

|  | Predicted Low Risk | Predicted High Risk |
|---|---:|---:|
| Actual Low Risk | 136,468 | 26,293 |
| Actual Default | 27,941 | 15,399 |

---

## Error Analysis Summary

Main findings:

- The model performs much better on 60-month loans than on 36-month loans.
- Debt consolidation has the highest number of false negatives.
- Small business loans have higher recall but are also riskier.
- Higher DTI groups are flagged more often.
- `term_months` is the most important feature by LightGBM gain.

Important note:

Error analysis was performed after final test evaluation, so it was used for interpretation only, not for test-driven model tuning.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Checks whether the API and model are loaded |
| `GET` | `/model-info` | Returns model metadata, threshold, metrics, and feature list |
| `POST` | `/predict` | Returns default risk prediction and business decision |

The `/predict` endpoint returns:

| Field | Meaning |
|---|---|
| `probability` | Model score for default risk. The score is not probability-calibrated. |
| `prediction` | Binary risk label: `1` means high risk, `0` means low risk |
| `label` | Human-readable risk category |
| `threshold` | Business threshold used for the decision |
| `decision` | Final business action: `manual_review` or `approve` |

---

## Run API Locally

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the FastAPI application:

```powershell
uvicorn src.api.app:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

## Example Prediction Request

PowerShell example:

```powershell
$body = @{
    loan_amnt = 18000
    term = "60 months"
    emp_length = "3 years"
    home_ownership = "RENT"
    annual_inc = 42000
    purpose = "debt_consolidation"
    dti = 34.5
    delinq_2yrs = 2
    earliest_cr_line = "Jan-2010"
    inq_last_6mths = 4
    open_acc = 9
    pub_rec = 1
    revol_bal = 16000
    revol_util = 88.5
    total_acc = 18
    issue_d = "Dec-2018"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://localhost:8000/predict `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

Example response:

```json
{
  "probability": 0.605672422292649,
  "prediction": 1,
  "label": "high_risk",
  "threshold": 0.2574331564883078,
  "decision": "manual_review"
}
```

---

## Dockerized FastAPI Inference Service

This project includes a Dockerized FastAPI service for credit default risk inference.

The Docker image packages:

- the FastAPI application;
- the trained LightGBM pipeline;
- model metadata and decision threshold;
- feature engineering code;
- required Python dependencies.

The container exposes the API on port `8000`.

### Build the Docker Image

From the project root:

```powershell
docker build -t credit-risk-api .
```

### Run the Container

```powershell
docker run -d --rm --name credit-risk-api-container -p 8000:8000 credit-risk-api
```

The API will be available at:

```text
http://localhost:8000
```

### Check API Health

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Expected response:

```text
status       healthy
model_loaded True
model_type   lightgbm
```

### View Model Metadata

```powershell
Invoke-RestMethod http://localhost:8000/model-info
```

The `/model-info` endpoint returns:

- model type;
- model parameters;
- selected threshold;
- review capacity;
- business assumptions;
- validation and test metrics;
- feature columns;
- time split configuration.

### Send a Prediction Request

```powershell
$body = @{
    loan_amnt = 18000
    term = "60 months"
    emp_length = "3 years"
    home_ownership = "RENT"
    annual_inc = 42000
    purpose = "debt_consolidation"
    dti = 34.5
    delinq_2yrs = 2
    earliest_cr_line = "Jan-2010"
    inq_last_6mths = 4
    open_acc = 9
    pub_rec = 1
    revol_bal = 16000
    revol_util = 88.5
    total_acc = 18
    issue_d = "Dec-2018"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://localhost:8000/predict `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

Example response:

```json
{
  "probability": 0.605672422292649,
  "prediction": 1,
  "label": "high_risk",
  "threshold": 0.2574331564883078,
  "decision": "manual_review"
}
```

### Stop the Container

```powershell
docker stop credit-risk-api-container
```

### Docker Production-Style Improvements

The Docker setup includes:

- a `HEALTHCHECK` that verifies the `/health` endpoint;
- a non-root `appuser` for safer container execution;
- pinned dependency versions for reproducible inference;
- `.dockerignore` to keep the image build context clean.

---

## Automated Tests

Run API tests:

```powershell
python -m pytest tests/test_api.py -v
```

The tests validate:

- health endpoint;
- model metadata endpoint;
- high-risk prediction;
- low-risk prediction;
- unseen categorical values;
- missing required fields;
- invalid numeric values;
- invalid date format.

Expected result:

```text
8 passed
```

---

## Final Model Summary

| Item | Value |
|---|---|
| Model | LightGBM |
| Split | Time-based |
| Validation ROC-AUC | 0.6809 |
| Test ROC-AUC | 0.6856 |
| Test PR-AUC | 0.3498 |
| Review capacity | Top 20% riskiest applications |
| Deployment | FastAPI + Docker |

---

## Limitations

Current limitations:

- The model score is not probability-calibrated.
- Business cost assumptions are illustrative.
- The model was trained on historical Lending Club data and may not generalize to other lending environments.
- Some borrower segments have weaker recall than others.
- The current Docker image prioritizes reproducibility over minimal image size.
- The inference container loads saved artifacts directly and does not connect to PostgreSQL.

---

## Next Steps

Possible future improvements:

- calibrate model scores using validation data;
- compare capacity-based thresholding with cost-minimization thresholding;
- add prediction drift monitoring;
- add GitHub Actions for tests and Docker build;
- create separate `requirements-api.txt` for a smaller inference image;
- improve segment-specific error analysis;
- add a more detailed business report.

---

## Key Takeaway

This project demonstrates an end-to-end ML workflow:

```text
raw lending data
→ PostgreSQL modeling table
→ feature engineering
→ leakage-aware time split
→ LightGBM model
→ business threshold
→ error analysis
→ FastAPI inference service
→ Dockerized deployment
```

The final system is not only a trained model, but a reproducible ML service that can be tested, containerized, and explained from both technical and business perspectives.
