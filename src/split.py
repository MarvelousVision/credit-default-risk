def time_based_split(df):
    df_sorted= df.sort_values('issue_date').reset_index(drop=True)
    train_df = df_sorted[df_sorted['issue_date'] < '2016-03-01']
    val_df = df_sorted[(df_sorted['issue_date'] >= '2016-03-01') & (df_sorted['issue_date'] < '2017-01-01')]
    test_df = df_sorted[df_sorted['issue_date'] >= '2017-01-01']
    return train_df, val_df, test_df

def create_xy(df):
    feature_cols=['loan_amnt',
    'home_ownership',
    'purpose',
    'dti',
    'delinq_2yrs',
    'inq_last_6mths',
    'open_acc',
    'pub_rec',
    'revol_bal',
    'revol_util',
    'total_acc',
    'term_months',
    'emp_length_years',
    'annual_inc_log',
    'credit_history_length_years']
    X= df[feature_cols]
    y= df['target']
    return X,y



