select term, 
count(*) as loan_count ,
round(100.0*count(*)/ sum(count(*)) over(),2) as percentage
from loans_modeling_v1 lmv 
group by term
order by count(*) desc;

select emp_length, 
count(*) as loan_count ,
round(100.0*count(*)/ sum(count(*)) over(),2) as percentage
from loans_modeling_v1 lmv 
group by emp_length
order by count(*) desc;

select home_ownership, 
count(*) as loan_count ,
round(100.0*count(*)/ sum(count(*)) over(),2) as percentage
from loans_modeling_v1 lmv 
group by home_ownership
order by count(*) desc;

select purpose, 
count(*) as loan_count ,
round(100.0*count(*)/ sum(count(*)) over(),2) as percentage
from loans_modeling_v1 lmv 
group by purpose
order by count(*) desc;

/*
Categorical checks:
- term is clean and has only two values: 36 months and 60 months.
- emp_length has no SQL NULL values, but it contains "n/a", which should be treated as missing during preprocessing.
- home_ownership has three main groups: MORTGAGE, RENT, OWN. Very small groups such as ANY, OTHER, and NONE may be combined later.
- purpose is dominated by debt_consolidation and credit_card, but all categories are still usable for baseline modeling.
*/


with stats as (
select 
      'annual_inc' as feature_name,
      min(annual_inc) as min_val,
      max(annual_inc) as max_val,
      round(avg(annual_inc)::numeric, 2) as avg_val
from loans_modeling_v1
union all 
select 
      'dti' as feature_name,
      min(dti) as min_val,
      max(dti) as max_val,
      round(avg(dti)::numeric, 2) as avg_val
from loans_modeling_v1
union all 
select 
      'revol_util' as feature_name,
      min(revol_util) as min_val,
      max(revol_util) as max_val,
      round(avg(revol_util)::numeric, 2) as avg_val
from loans_modeling_v1
union all 
select 
      'loan_amnt' as feature_name,
      min(loan_amnt) as min_val,
      max(loan_amnt) as max_val,
      round(avg(loan_amnt)::numeric, 2) as avg_val
from loans_modeling_v1
union all 
select 
      'open_acc' as feature_name,
      min(open_acc) as min_val,
      max(open_acc) as max_val,
      round(avg(open_acc)::numeric, 2) as avg_val
from loans_modeling_v1
union all 
select 
      'total_acc' as feature_name,
      min(total_acc) as min_val,
      max(total_acc) as max_val,
      round(avg(total_acc)::numeric, 2) as avg_val
from loans_modeling_v1
)
select * 
from stats 
order by feature_name;
/*
Numeric range checks:
- loan_amnt range looks reasonable: 500 to 40000.
- annual_inc contains extreme values, including 0 and very high incomes. These should be checked as potential outliers.
- dti contains suspicious values, including -1 and very high values up to 999.
- revol_util contains extreme values above 100, with a maximum of 892.3.
- open_acc and total_acc have high maximum values, but they are not automatically invalid.
- Outliers should not be removed blindly; they will be handled later during preprocessing/modeling.
*/
select
    'annual_inc = 0' as check_name,
    count(*) as row_count,
    round(100.0 * count(*) / (select count(*) from loans_modeling_v1), 4) as percentage
from loans_modeling_v1
where annual_inc = 0;

select
    'where annual_inc > 500000' as check_name,
    count(*) as row_count,
    round(100.0 * count(*) / (select count(*) from loans_modeling_v1), 4) as percentage
from loans_modeling_v1
where annual_inc > 500000;

select
    'dti < 0' as check_name,
    count(*) as row_count,
    round(100.0 * count(*) / (select count(*) from loans_modeling_v1), 4) as percentage
from loans_modeling_v1
where dti < 0;

select
    'dti > 100' as check_name,
    count(*) as row_count,
    round(100.0 * count(*) / (select count(*) from loans_modeling_v1), 4) as percentage
from loans_modeling_v1
where dti > 100;

select
    'revol_util > 100' as check_name,
    count(*) as row_count,
    round(100.0 * count(*) / (select count(*) from loans_modeling_v1), 4) as percentage
from loans_modeling_v1
where revol_util > 100;

select
    'revol_util > 200' as check_name,
    count(*) as row_count,
    round(100.0 * count(*) / (select count(*) from loans_modeling_v1), 4) as percentage
from loans_modeling_v1
where revol_util > 200;

select
    'open_acc = 0' as check_name,
    count(*) as row_count,
    round(100.0 * count(*) / (select count(*) from loans_modeling_v1), 4) as percentage
from loans_modeling_v1
where open_acc = 0;

select
    'total_acc > 100' as check_name,
    count(*) as row_count,
    round(100.0 * count(*) / (select count(*) from loans_modeling_v1), 4) as percentage
from loans_modeling_v1
where total_acc > 100;
/*
Outlier checks:
- annual_inc has 302 zero-income rows and 1,666 rows above 500,000. These are rare but should be treated as potential outliers.
- dti has 2 negative values and 476 rows above 100. Negative DTI is likely invalid; very high DTI values are rare.
- revol_util has 4,537 rows above 100 and only 2 rows above 200. Values above 100 may be possible but should be treated carefully.
- open_acc = 0 and total_acc > 100 are very rare.
- Since suspicious values are a small share of the dataset, I will not remove them during SQL preparation. They will be handled later in the Python preprocessing/modeling stage.
*/