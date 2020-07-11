"""Prepare data for Plotly Dash."""
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text, inspect
import psycopg2

def create_dataframe():
    """Create Pandas DataFrame from local CSV."""
    df = pd.read_csv('data/311-calls.csv', parse_dates=['created'])
    df['created'] = df['created'].dt.date
    df.drop(columns=['incident_zip'], inplace=True)
    num_complaints = df['complaint_type'].value_counts()
    to_remove = num_complaints[num_complaints <= 30].index
    df.replace(to_remove, np.nan, inplace=True)
    return df


def create_icbf_dataframe():
    DB_USERNAME = 'acastelblanco'
    DB_PASSWORD = 'Team67!'
    DB_ENDPOINT = 'ds4a-demo-instance.cqjr4hyu9xaq.us-east-1.rds.amazonaws.com'
    DB_NAME = 'desertion_pj_team67'
    engine = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}', max_overflow=20)

    def run_query(sql):
        result = engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(sql)))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

    df_icbf = run_query("""
    select * from educacion_basica_vars limit 100;""")

    df_desertion = run_query("""
    select code_dept, max(desertion_perc) as desertion
    from desertion_by_municip
    where year_cohort = 2019
    group by code_dept
    ;""")

    return df_icbf

def create_desertion_dataframe():
    DB_USERNAME = 'acastelblanco'
    DB_PASSWORD = 'Team67!'
    DB_ENDPOINT = 'ds4a-demo-instance.cqjr4hyu9xaq.us-east-1.rds.amazonaws.com'
    DB_NAME = 'desertion_pj_team67'
    engine = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}', max_overflow=20)

    def run_query(sql):
        result = engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(sql)))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

    df_desertion = run_query("""
    select code_dept, max(desertion_perc) as desertion
    from desertion_by_municip
    where year_cohort = 2019
    group by code_dept
    ;""")

    return df_desertion