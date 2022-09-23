import streamlit as st

import pandas as pd
import numpy as np
from helper_func.sel_attr import *


def st_2_df(country_continant, country_region, countries, table_dict, sql_engine, att_no):

    st.sidebar.markdown(f"<h3 style='background-color:#A3BCF9;color: white; vertical-align:middle;\
        padding:1px 1px;text-align: center;'>Attribute No. {att_no}</h1>", unsafe_allow_html=True)
    table_option = st.sidebar.selectbox('Select one:', list(table_dict.keys()),key=(att_no*1))
    table_option_decoded = table_dict[table_option]

    st.sidebar.markdown("<h4 style='background-color:#424B54;color: white; vertical-align: middle;\
     padding:1px 1px;text-align: center;'>of what part of the world</h1>", unsafe_allow_html=True)

    what_part = st.sidebar.radio("", options=(
        'Country', 'Region', 'Continant'), horizontal=True,key=(att_no*3))

    if what_part == "Country":
        option = st.sidebar.selectbox('Select one:', list(countries.keys()),key=(att_no*5))
        country_list = countries[option]

    if what_part == "Region":
        option = st.sidebar.selectbox(
            'Select one:', list(country_region.keys()),key=(att_no*7))
        country_list = country_region[option]

    if what_part == "Continant":
        option = st.sidebar.selectbox(
            'Select one:', list(country_continant.keys()),key=(att_no*11))
        country_list = country_continant[option]

    is_avg = st.sidebar.checkbox('Do you want the average by country?',key=(att_no*13))
    df, suffix_table = select_many(
        table_option_decoded, country_list, sql_engine, is_avg)

    return df, suffix_table,option
