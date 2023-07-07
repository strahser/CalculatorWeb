import pandas as pd
import streamlit as st
import sqlite3 as sq
@st.cache_data
def load_input_data_frame(path_to_excel):
	return pd.read_excel(path_to_excel)

@st.cache_data
def load_sql_data_frame(table_name:str,connector:sq.Connection):
	return pd.read_sql(table_name,connector)