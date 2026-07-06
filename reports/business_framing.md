1. Which dataset do I choose?
Dataset: Lending Club Loan Data
PostgreSQL role:I will use PostgreSQL to store the raw loan data,
run SQL checks, create cleaned/filtered tables, and build the final
modeling dataset for machine learning.

2. Who is the business user of the model?
The business user is a bank or lending company risk team.

3. What decision does the model support?
identify borrowers who may not repay the loan.
Probably send these klient on re-cheak and manual review.
Also Change loan conditions. 

4. Target variable
Target: Binary flag for each loan — 1 if the loan defaulted/charged off,
0 if fully repaid. Exact default definition will be confirmed after exploring
Lending Club loan status values.

5. What does false positive mean?
The model marks a good borrower as risky.

6. What does false negative mean?
FN: Model predicts low risk, but borrower actually defaults. 
Cost: Very high — bank approves risky borrower and loses the full loan amount.

7. Which mistake is more expensive and why?
False Negative because its so expancive and bank will loose mony althought if banc 
rejects good client (False Positive) bank just wont earn mony
false positives can also be expensive if there are too many,
because the bank rejects too many good borrowers. 

8. What should the model output: probability or class label?
a model should output probability of default because its important to see 
a risk to make a decision 

9. Which metrics should I track?
Metrics:
Ranking: ROC-AUC, PR-AUC.
Threshold: Precision, Recall, F1-Score.
Business: Business Cost/Profit Metric (Total Cost = (FN × cost_FN) + (FP × cost_FP)).

10. Where can data leakage appear?
Preprocessing leakage: Fit imputers/scalers only on train data, never on full dataset.
Business leakage: Never use post-approval information (payments, collections, recoveries).
Validation: Use time-based split if issue date is available and suitable for the data.

11. What SQL questions do I want to answer first?
What is the profile of defaulters vs. good payers (income, debt-to-income ratio, credit history)?
How does default rate vary with loan characteristics (amount, term, rate, grade, purpose)?
How do credit history indicators (delinquencies, inquiries, open lines) correlate with default?

False Negative: default borrower predicted as safe. This is the most expensive error because the bank approves a risky loan.

False Positive: fully paid borrower predicted as risky. This is less expensive because the bank may reject a good borrower or send them to manual review.

Because exact profit/loss values are not available, I will use assumptions:
FN cost = 60% of loan amount
FP cost = 5% of loan amount