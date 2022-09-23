from decimal import Decimal
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.types import *

def main():
    sql_engine = create_engine(
        'postgresql://myuser:mypass@localhost/world_data_etl')
    pd.options.mode.chained_assignment = "warn"

    ################################################  Extract ################################################
    HDI_csv_path = "raw_data/human-development-index.csv"
    military_expendutes_csv_path = "raw_data/Military Expenditure.csv"
    population_csv_path = "raw_data/population_total_long.csv"
    life_exp_csv_path = "raw_data/Human_life_Expectancy.csv"
    gdp_csv_path = "raw_data/world_country_gdp_usd.csv"
    countries_path = 'raw_data/all.csv'

    countries_df = pd.read_csv(countries_path)
    hdi_df = pd.read_csv(HDI_csv_path)
    pop_df = pd.read_csv(population_csv_path)
    gdp_df = pd.read_csv(gdp_csv_path)
    mil_df = pd.read_csv(military_expendutes_csv_path)
    lex_df = pd.read_csv(life_exp_csv_path)

    ################################################  Transform ##############################################
    # //// 1. countries table


    countries_df.drop(['country-code', 'alpha-2'], axis=1, inplace=True)
    countries_df['name'] = countries_df['name'].str.lower()

    countries_df.rename(columns={'alpha-3': 'country_code',
                                'iso_3166-2': 'iso_3166', 'sub-region': 'sub_region',
                                'intermediate-region': 'intermediate_region',
                                'region-code': 'region_code', 'sub-region-code': 'sub_region_code',
                                'intermediate-region-code': 'intermediate_region_code'
                                }, inplace=True, errors='raise')

    cols = ['region_code', 'sub_region_code', 'intermediate_region_code']
    countries_df[cols] = countries_df[cols].apply(pd.to_numeric).astype('Int64')
    iso_code = countries_df[['name', 'country_code']]
    iso_dict = iso_code.set_index("name").to_dict()
    iso_dict = iso_dict['country_code']
    iso_list = list(iso_code['country_code'])


    # //// 2. HDI index

    hdi_df_wide = pd.pivot(hdi_df,\
        index=['Code', 'Entity'], columns='Year', values='Human Development Index (UNDP)')

    hdi_df_wide = hdi_df_wide.reset_index()

    # South korea is repeated twice with no "North Korea" which in not that bad anyways :D
    hdi_df_wide.drop(index=0, axis=1, inplace=True)

    hdi_df_wide.drop(['Entity'], axis=1, inplace=True)
    hdi_df_wide.rename(columns={'Code': 'country_code'},
                    inplace=True, errors='raise')
    hdi_df_wide=hdi_df_wide.add_suffix('_hdi')


    # //// 3. population

    pop_df_wide = pd.pivot(pop_df, index='Country Name',
                        columns='Year', values='Count')  # Reshape from long to wide
    pop_df_wide = pop_df_wide.reset_index()

    # these are region or unricognized countries
    pop_df_wide.drop(index=[36, 40, 106, 129, 150], axis=1, inplace=True)

    pop_df_wide["code"] = pop_df_wide["Country Name"]\
        .str.lower().map(iso_dict)

    pop_df_wide["code"][pop_df_wide.\
        code.isna()] = ["BHS", "BOL", "VGB", "COD", "COG", "CIV", "CUW", "CZE", "EGY", "GMB",
                                "HKG", "IRN", "PRK", "KOR", "KGZ", "LAO", "MAC", "MDA", "SVK", "KNA",
                                "LCA", "MAF", "VCT", "TZA", "GBR", "USA", "VEN", "VNM", "PSE", "YEM"]
    pop_df_wide.insert(0, 'country_code', pop_df_wide["code"])

    pop_df_wide.drop(['Country Name','code'], axis=1, inplace=True)
    pop_df_wide=pop_df_wide.add_suffix('_pop')

    # //// 4.GDP

    gdp_df_wide = pd.pivot(gdp_df, index=['Country Name', 'Country Code'],
                        columns='year', values='GDP_USD')  # Reshape from long to wide
    gdp_df_wide = gdp_df_wide.reset_index()

    gdp_df_wide = gdp_df_wide[gdp_df_wide["Country Code"].isin(iso_list)]

    gdp_df_wide.drop(['Country Name'], axis=1, inplace=True)
    gdp_df_wide.rename(
        columns={'Country Code': 'country_code'}, inplace=True, errors='raise')

    gdp_df_wide=gdp_df_wide.add_suffix('_gdp')

    # //// 5. Military expenditure
    mil_df = mil_df[mil_df["Type"] == 'Country']
    mil_df.drop(['Indicator Name', 'Type'], axis=1, inplace=True)
    mil_df = mil_df[mil_df["Code"].isin(iso_list)]

    mil_df.drop(['Name'], axis=1, inplace=True)
    mil_df.rename(columns={'Code': 'country_code'}, inplace=True, errors='raise')

    mil_df=mil_df.add_suffix('_mil')

    # //// 6. life expectancy
    lex_df = lex_df[lex_df["Level"] == "National"]
    lex_df.drop(['Level', 'Region'], axis=1, inplace=True)

    # no na is shown because nan is replaced by Not Available  it needs to be replaced back
    lex_df.replace("Not Available", np.nan, inplace=True)

    lex_df = lex_df[lex_df["Country_Code"].isin(iso_list)]

    lex_df.drop(['Country'], axis=1, inplace=True)
    lex_df.rename(columns={'Country_Code': 'country_code'},
                inplace=True, errors='raise')

    lex_df=lex_df.add_suffix('_lif')

    ################################################  load  ################################################
    def df_2_sql_table(df,table_name,dtype,sql_engine):
        table_schema = dict.fromkeys(list(df.columns)[1:], dtype)
        table_schema[list(df.columns)[0]]=String(3)
        df.to_sql(name=table_name, con=sql_engine,
                    dtype=table_schema, if_exists='append', index=False)
        print(f'loaded :{table_name}')

    countries_table_schema = {
        "country_code": String(3),
        "name": TEXT,
        "iso_3166": TEXT,
        "region": TEXT,
        "sub_region":TEXT ,
        "intermediate_region": TEXT,
        "region_code": Integer,
        "sub_region_code": Integer,
        "intermediate_region_code": Integer
    }
    countries_df.to_sql(name='countries_table', con=sql_engine,
                        dtype=countries_table_schema, if_exists='append', index=True)


    df_2_sql_table(hdi_df_wide,'hdi_table',FLOAT(),sql_engine)
    df_2_sql_table(gdp_df_wide,'gdp_table',BIGINT,sql_engine)
    df_2_sql_table(pop_df_wide,'population_table',BIGINT,sql_engine)
    df_2_sql_table(mil_df,'mil_exp_table',BIGINT,sql_engine)
    df_2_sql_table(lex_df,'lif_exp_table',FLOAT(),sql_engine)



    with sql_engine.connect() as conn:
        conn.execute('''
        ALTER TABLE countries_table ADD PRIMARY KEY(index);
        ALTER TABLE hdi_table ADD PRIMARY KEY(country_code_hdi);
        ALTER TABLE gdp_table ADD PRIMARY KEY(country_code_gdp);
        ALTER TABLE population_table ADD PRIMARY KEY(country_code_pop);
        ALTER TABLE lif_exp_table ADD PRIMARY KEY(country_code_lif);
        ALTER TABLE mil_exp_table ADD PRIMARY KEY(country_code_mil);
        ''')
if __name__ == '__main__':
    main()