import pandas as pd

def select_countries(sql_engine):

    county_list_query=f'''
            SELECT *
            FROM countries_table as c
            '''
    countries_df =pd.read_sql(county_list_query,sql_engine)
    countries=pd.Series(countries_df.country_code.values, index=countries_df.name).to_dict()
    continants=countries_df['region'].unique()
    regions=countries_df['sub_region'].unique()
    country_region={}
    country_continant={}

    for continant in continants:
        country_continant[continant]= list(countries_df['country_code'][countries_df['region']==continant])

    for region in regions:
        country_region[region]= list(countries_df['country_code'][countries_df['sub_region']==region])
    
    return country_continant,country_region,countries