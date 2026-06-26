SELECT COUNT(*)
FROM loans_raw;

SELECT count(* ) as count , loan_status
FROM loans_raw
group by  loan_status ;

/* target = 0:
- Fully Paid

target = 1:
- Charged Off
- Default 

remove:
- Current
- In Grace Period
- Late (16-30 days)
- Late (31-120 days)
- Does not meet the credit policy. Status:Fully Paid
- Does not meet the credit policy. Status:Charged Off*/

