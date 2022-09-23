import pandas as pd

def wide_to_one_col(df,suffix_table,is_avg=True):
    df.drop(f"country_code_{suffix_table}", axis=1, inplace=True)
    df.columns = df.columns.str.rstrip(f'_{suffix_table}')
    df.columns.rename('year', inplace=True)
    df = df.transpose()
    df.index= df.index.astype(int)
    
    if is_avg == True:
        temp= list(df.mean(axis=1)[:])
    elif is_avg==False:
        temp= list(df.sum(axis=1)[:])


    df.drop(list(df.columns),axis=1, inplace=True)
    df[f"{suffix_table}"] = temp
    df=df.sort_index().fillna(0)
    
    return df

def select_many(table_option,country_options,sql_engine,is_avg):
    if type(country_options) == str:
        country_options = f"('{country_options}')"
    else:
        country_options = tuple(country_options)
    
    suffix_table= table_option[:3]
    query =f'''
    SELECT *
    FROM {table_option}
    where "country_code_{suffix_table}" in {country_options}
    '''
    df=pd.read_sql(query,sql_engine)
    df=wide_to_one_col(df,suffix_table,is_avg)

    return df,suffix_table
