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
from helper_func.st_2_df import *

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
     padding:5px 5px;text-align: center;'>Data visualization of world data</h1>", unsafe_allow_html=True)
    st.markdown('')



    plot_count = st.slider("how many attributes you want to plot?",1,2,1)

    if plot_count == 1:
        df,suffix_table,option=st_2_df(country_continant,country_region,countries,table_dict,sql_engine,1)

        fig = px.line(
            df, 
            x=df.index,
            y=f'{suffix_table}',
            height=700, width=800,
            labels={f'{suffix_table}': f'{suffix_dict[suffix_table]}'},
            title=f"{suffix_dict[suffix_table]} of  {option}")

       
        st.write(fig)
   
    if plot_count == 2:

        att_no = st.sidebar.selectbox('Which attribute:',(1, 2))

        df,suffix_table,option=st_2_df(country_continant,country_region,countries,table_dict,sql_engine,att_no)
        
        if att_no == 1:
            if st.sidebar.button('Select'):
                if 'key' not in st.session_state:
                    st.session_state['first_att'] = df,suffix_table,option
                   

        if att_no == 2:
            if st.sidebar.button('Select'):
                if 'key' not in st.session_state:
                    st.session_state['sec_att'] = df,suffix_table,option
        try:

            df1,suffix_table1,option1=st.session_state['first_att'][0],st.session_state['first_att'][1],st.session_state['first_att'][2]
            st.sidebar.write(f"Attribute 1:{suffix_dict[suffix_table1]} of {option1}")

            df2,suffix_table2,option2=st.session_state['sec_att'][0],st.session_state['sec_att'][1],st.session_state['sec_att'][2]
            st.sidebar.write(f"Attribute 2:{suffix_dict[suffix_table2]} of {option2}")
            st.success("Generating  Plot")
            result = pd.concat([df1, df2], axis=1)
            fig = px.scatter(
            result, 
            x=f'{suffix_table1}',
            y=f'{suffix_table2}',
            height=700, width=800,
            labels={
                f'{suffix_table1}': f'{suffix_dict[suffix_table1]}',
                f'{suffix_table2}': f'{suffix_dict[suffix_table2]}'},
            title=f"{suffix_dict[suffix_table1]} of {option1} vs {suffix_dict[suffix_table2]} of {option2} ")
        
            st.write(fig)
        except:
            st.warning("Make sure you selected 2 Attribute")


if __name__ == '__main__':
    main()