select COUNT(*) as total_rows 
from  loans_modeling_v1;

select  
    target,
    COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM loans_modeling_v1
GROUP BY target
ORDER BY target;

SELECT 
    loan_status,
    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS default_count,
    SUM(CASE WHEN target = 0 THEN 1 ELSE 0 END) AS fully_paid_count
FROM loans_modeling_v1
GROUP BY loan_status
ORDER BY loan_status;

SELECT 
    grade,
    COUNT(*) AS loan_count,
    ROUND(100.0 * AVG(target), 2) AS default_rate_percent
FROM loans_modeling_v1
GROUP BY grade
ORDER BY grade;

select round (avg(target)* 100,2) as overall_default_rate
from loans_modeling_v1;

/*
Default rate increases from grade A to G, 
which confirms that grade is strongly related to credit 
risk. Because grade may represent Lending Club’s internal
 risk assessment, I will treat it carefully and later
  compare models with and without grade/sub_grade/int_rate.
*/
