# region import
import os
import inspect
import sys
import streamlit as st
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from EnergyCompare.Control.EnergyCompareControl import energy_compare_control  # noqa: E402
from DB.ExcelDBPath import ExcelDBPath
from CSS import CssStyle


# endregion


@st.cache_data
def load_input_data_frame(path_to_excel):
	return pd.read_excel(path_to_excel)


def energy_compare_main(gsop):
	path_to_db_excel = ExcelDBPath.order_399_table1
	df = load_input_data_frame(path_to_db_excel)
	energy_compare_control(df, gsop=gsop)
