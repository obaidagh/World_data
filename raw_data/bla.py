import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = "warn"

################################################  Extract ################################################
HDI_csv_path = "raw_data/human-development-index.csv"
military_expendutes_csv_path = "raw_data/Military Expenditure.csv"
population_csv_path = "raw_data/population_total_long.csv"
life_exp_csv_path = "raw_data/Human_life_Expectancy.csv"
gdp_csv_path = "raw_data/world_country_gdp_usd.csv"


hdi_df = pd.read_csv(HDI_csv_path)
pop_df = pd.read_csv(population_csv_path)
gdp_df = pd.read_csv(gdp_csv_path)
mil_df = pd.read_csv(military_expendutes_csv_path)
lex_df = pd.read_csv(life_exp_csv_path)
################################################  Transform ################################################

#///// 1. countries table

countries = pd.read_csv('raw_data/all.csv')

iso_code = countries[['name', 'alpha-3']]
iso_code['name'] = iso_code['name'].str.lower()

iso_dict = iso_code.set_index("name").to_dict()
iso_dict = iso_dict['alpha-3']

iso_list = list(countries['alpha-3'])