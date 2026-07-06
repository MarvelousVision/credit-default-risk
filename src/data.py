import os
import pandas as pd 
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_engine():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not set in environment. Please check your .env file.")
    engine = create_engine(database_url)
    return engine

def load_modeling_data(table_name: str):
    allowed_tables = {"loans_modeling_v1"}
    if table_name not in allowed_tables:
        raise ValueError(f"Unsupported table: {table_name}")
    engine= get_engine()
    query = f"""
    SELECT
        target,
        loan_status,
        loan_amnt,
        term,
        emp_length,
        home_ownership,
        annual_inc,
        purpose,
        dti,
        delinq_2yrs,
        earliest_cr_line,
        inq_last_6mths,
        open_acc,
        pub_rec,
        revol_bal,
        revol_util,
        total_acc,
        issue_d
    FROM {table_name};
    """
    df = pd.read_sql(query, engine)
    return df 

