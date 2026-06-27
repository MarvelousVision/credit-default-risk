select purpose,
count(*) as loan_count ,
round(AVG(target)*100.0,2) as default_rate_percent
from loans_modeling_v1
group by purpose
order by AVG(target) desc;

select term,
count(*) as loan_count ,
round(AVG(target)*100.0,2) as default_rate_percent
from loans_modeling_v1
group by term
order by AVG(target) desc;

select home_ownership,
count(*) as loan_count ,
round(AVG(target)*100.0,2) as default_rate_percent
from loans_modeling_v1
group by home_ownership
order by AVG(target) desc;

with income as (select  *,
case when annual_inc is null then 'missing'
     when annual_inc<40000 then '<40'
     when annual_inc>=40000 and annual_inc<80000 then '40-80'
     when annual_inc>=80000 and annual_inc<120000 then '80-120'
     else '>120'
     end as income_group
     from loans_modeling_v1 lmv )
select income_group,
COUNT(*) AS loan_count, 
round(AVG(target)*100.0,2) as default_rate_percent
from income 
group by income_group
order by round(AVG(target)*100.0,2) desc;


with dti as (select  *,
case when dti is null then 'missing'
     when dti<10 then '0-10'
     when dti>=10 and dti<20 then '10-20'
     when dti>=20 and dti<30 then '20-30'
     else '>30'
     end as dti_group
     from loans_modeling_v1 lmv )
select dti_group,
COUNT(*) AS loan_count, 
round(AVG(target)*100.0,2) as default_rate_percent
from dti 
group by dti_group
order by round(AVG(target)*100.0,2) desc;

/*The highest-risk segments are 60-month loans, high-DTI borrowers,
 lower-income borrowers, and some purposes such as small business, moving, medical,
  and debt consolidation.

The results make business sense: longer loan terms and higher debt-to-income ratios are
 associated with higher default risk. Lower income groups also show higher default rates.

For home ownership, RENT has higher default risk than MORTGAGE among large groups. Very
 small categories such as NONE, OTHER, and ANY should not be overinterpreted because they 
 have few observations.

Grade is strongly related to default risk, but it may represent Lending Club’s internal 
risk assessment. I will later compare models with and without grade/sub_grade/int_rate.
*/
