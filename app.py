from EnergyCompare.EnergyCompareMain import energy_compare_main
from GSOPCalculator.GSOPApp import gsop_main
import streamlit as st
st.set_page_config(page_title='Energy Calculator', page_icon="chart_with_upwards_trend", layout="wide")
st.title("Калькулятор расчета удельных затрат энергии МКД в год")


gsop_calculation_option =st.sidebar.radio("Выберите опцию расчета",["Известен город","Известен ГСОП"])
if gsop_calculation_option=="Известен город":
	gsop = gsop_main()
	energy_compare_main(gsop)
else:
	energy_compare_main(gsop=None)