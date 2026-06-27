loan_status - drop from model/ it directly reveals the final loan outcome and was used only to create target
target - label variable, used as y; never used as input feature
loan_amnt - Keep/ Known at application/approval time. 
term - Keep/ Known at application/approval time.
int_rate → Unsure / pricing feature, exclude from conservative baseline
installment → Unsure / derived from pricing, exclude from conservative baseline
grade → Unsure / lender-generated, exclude from baseline
sub_grade → Unsure / lender-generated, exclude from baseline
emp_length  - keep/ Longer employment = lower risk.
home_ownership  - keep/ Owning a home often means more financial stability and collateral.
annual_inc  - keep/ Higher income = lower default risk.
verification_status → Unsure / underwriting process feature.
issue_d → Use for time split, not as direct model feature
purpose  - keep/Different purposes have different risk profiles.
dti  - keep/ Key metric.
delinq_2yrs  - keep/ Strong behavioral signal. 
earliest_cr_line → Transform into credit history length
inq_last_6mths  - keep/ Shows financial distress.
open_acc  -keep/ Shows current debt load. 
pub_rec  -keep/Bankruptcies and court records are massive red flags.
revol_bal  -keep/ High balance = high risk.
revol_util  -keep/	Revolving utilization rate. 
total_acc-keep/Experience with credit

Baseline feature strategy:
I will first train a conservative borrower/application model without grade, sub_grade, int_rate, and installment. Later I will compare it with an enriched model that includes lender-generated/pricing features.
