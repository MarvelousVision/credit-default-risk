import pandas as pd 
import numpy as np 
def create_features(dff):
    df=dff.copy()
    df['term_months']=df['term'].str.replace(' months', '').astype(int)
    e_l_map={
        '< 1 year' : 0,
        '1 year'   : 1,
        '2 years'   : 2,
        '3 years'   : 3,
        '4 years'   : 4,
        '5 years'   : 5,
        '6 years'   : 6,
        '7 years'   : 7,
        '8 years'   : 8,
        '9 years'   : 9,
        '10+ years'   : 10,
        'n/a': -1
    }
    df['emp_length_years'] =df['emp_length'].map(e_l_map)
    df['annual_inc_log']= np.log1p(df['annual_inc'])

    df['earliest_date'] = pd.to_datetime(df['earliest_cr_line'], format='%b-%Y')
    df['issue_date']= pd.to_datetime(df['issue_d'], format='%b-%Y')
    df['credit_history_length_years']=((df['issue_date']-df['earliest_date']).dt.days/ 365.0).round(2)
    home_map={
        'NONE': 'OTHER'  ,
         'ANY': 'OTHER'
    }
    df['home_ownership']=df['home_ownership'].replace(home_map)

    rare_p = [
    'educational',
    'renewable_energy',
    'wedding',
    'house',
    'vacation',
    'car'
    ]
    df['purpose']=df['purpose'].replace(dict.fromkeys(rare_p, 'OTHER'))

    df['dti']= np.where(df['dti']<0, np.nan, df['dti'])

    df = df.drop(['emp_length','issue_d', 'earliest_cr_line', 'earliest_date','term', 'annual_inc'], axis=1)
    return df 


