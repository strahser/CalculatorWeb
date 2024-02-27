
from enum import Enum
from Forms.FormsNames import FormsNames
from Forms.TabsNames import TabsNames

import streamlit as st

from EnergyCompare.Utility.MakeGrid import make_grid


class DataLabel(Enum):
	GSOP = "Градусо-сутки отопительного периода"
	q_р_от = "Расчётная характеристика расхода тепловой энергии на отопление и вентиляцию"
	V_от = "Отапливаемый объём здания"
	A_кв = "Площадь квартир жилого здания"
	A_нж = "Полезная площадь нежилых помещений, кв. м"
	Nж = "Количество жителей в здании, чел."
	Nчел = "Количество работающих в нежилых помещениях здания, чел."
	N_этаж = "Количество этажей"
	v_гв_ж = "Расчетный нормативный среднесуточный расход горячей воды на человека (л/(сут*чел.))"  # combobox
	v_гв_нж = "Расчетный нормативный среднесуточный расход горячей воды на работника (л/(сут*чел.))"  # combobox
	alpha = "коэффициент одновременности"
	z_heat = "количество дней отопительного периода"
	K_ef_h_w = "Коэффициент эффективности использования ГВС"
	q_ee = "Удельный годовой расход электрической энергии"

	def __str__(self):
		return f'{self.name}'

	def __init__(self):
		tabs = st.tabs([val.value for val in TabsNames])
		with tabs[0]:
			self._create_form()

	def _create_form(self):
		with st.form(FormsNames.form_customer_data.value):
			rows = len(DataLabel) + 1
			grid = make_grid(rows, (4, 2, 4))
			grid[0][0].subheader(FormsNames.form_customer_data_label.value)
			grid[0][1].subheader(FormsNames.form_customer_data_value.value)
			for en, data in enumerate(DataLabel):
				with grid[en + 1][0]:
					st.write(str(data.value))
				with grid[en + 1][1]:
					setattr(self, data.name,
					        st.number_input(data.value, min_value=0.00, label_visibility="collapsed")
					        )