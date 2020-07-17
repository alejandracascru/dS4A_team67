import pandas as pd
from sqlalchemy import create_engine, text

# maximum number of rows to display
pd.options.display.max_rows = 20

DB_USERNAME = 'alagos'
DB_PASSWORD = 'Team67!'
DB_ENDPOINT = 'ds4a-demo-instance.cqjr4hyu9xaq.us-east-1.rds.amazonaws.com'
DB_NAME = 'desertion_pj_team67'
engine=create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}', max_overflow=20)

def runQuery(sql):
    result = engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(sql)))
    return pd.DataFrame(result.fetchall(), columns=result.keys())