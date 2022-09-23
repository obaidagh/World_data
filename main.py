# Core Pkgs
import streamlit as st

# EDA Pkgs
import pandas as pd
import numpy as np

# Data Viz Pkg
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
from sqlalchemy import create_engine

#helpers
from helper_func.select_countries import select_countries
from helper_func.sel_attr import *

def main():

    sql_engine = create_engine(
        'postgresql://myuser:mypass@localhost/world_data_etl')


    country_continant,country_region,countries = select_countries(sql_engine)
    table_dict= {
        'HDI':'hdi_table',
        'Population':'population_table',
        'GDP':'gdp_table',
        'Military Expendtures':'mil_exp_table',
        'Life Expectancy':'lif_exp_table'
                }
    
    suffix_dict = {
        "hdi":"Human development index",
        "lif":"Life expectancy",
        "mil":"Military Expendtures",
        "pop":"Population",
        "gdp":"Gross domestic product"

    }


    st.markdown("<h1 style='background-color:#BEE5BF;color: white; vertical-align: middle;\
     padding:5px 5px;text-align: center;'>Some title</h1>", unsafe_allow_html=True)
    st.markdown('')

    st.markdown("<h3 style='background-color:#FFD1BA;color: white; vertical-align: middle;\
     padding:1px 1px;text-align: center;'>how many attributes you want to plot</h1>", unsafe_allow_html=True)
    plot_count = st.radio("", ('one', 'two'), horizontal=True)

    

    if plot_count == 'one':

        st.markdown("<h3 style='background-color:#A3BCF9;color: white; vertical-align:middle;\
         padding:1px 1px;text-align: center;'>of what part of the world</h1>", unsafe_allow_html=True)

        what_part = st.radio("", options=(
            'Country', 'Region', 'Continant'), horizontal=True)
        st.markdown("<h4 style='background-color:#424B54;color: white; vertical-align: middle; padding:1px 1px;text-align: center;'>of what part of the world</h1>", unsafe_allow_html=True)

        if what_part == "Country":
            option = st.selectbox('Select one:', list(countries.keys()))
            country_list=countries[option]


        if what_part == "Region":
            option = st.selectbox('Select one:', list(country_region.keys()))
            country_list = country_region[option]

        if what_part == "Continant":
            option = st.selectbox('Select one:', list(country_continant.keys()))
            country_list = country_continant[option]


        table_option = st.selectbox('Select one:',list(table_dict.keys()) )
        table_option_decoded=table_dict[table_option]
        is_avg = st.checkbox('Do you want the average by country?')
        st.markdown("<h6 style='vertical-align: middle; padding:1px 1px;text-align: center;'>selected countries</h1>", unsafe_allow_html=True)
        st.write(country_list)
        df,suffix_table=select_many(table_option_decoded,country_list,sql_engine,is_avg)

        fig = px.line(
            df, 
            x=df.index,
            y=f'{suffix_table}',
            height=400, width=800,
            labels={f'{suffix_table}': f'{suffix_dict[suffix_table]}'},
            title="")
        
        st.write(fig)

        




if __name__ == '__main__':
    main()

    #st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))
    # if st.button("Generate Plot"):
