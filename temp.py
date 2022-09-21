from sqlalchemy import create_engine
from sqlalchemy.types import *
import pandas as pd

sql_engine = create_engine(
    'postgresql://myuser:mypass@localhost/world_data_etl')

country_code='ALB'
query=f'''
        SELECT *
        FROM hdi_table as h
        join countries_table as c
        on c.country_code = h.country_code_hdi
        where country_code='{country_code}';
        '''
df =pd.read_sql(query,sql_engine)
print(df)