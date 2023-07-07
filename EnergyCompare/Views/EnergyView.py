import pandas as pd
import plotly.express as px
import streamlit as st
import locale
locale.setlocale(locale.LC_ALL, '')

from EnergyCompare.Models.EnergyModels import Constant, ClASS_DATA, BaseNames
from EnergyCompare.Process.EnergyClasses import EnergyClasses
from streamlit_modal import Modal
from streamlit_elements import elements, mui, html
from EnergyCompare.Utility.MakeGrid import make_grid


class EnergyView(EnergyClasses):
	def __init__(self, input_data_frame: pd.DataFrame,gsop:float):
		self.gsop = gsop
		
		"""Входные данные, результаты, удельные потери энергии"""
		super().__init__(input_data_frame)

	def create_tabs(self):
		self._create_main_tab()
		self._create_result_chart()

	def _create_main_tab(self):
		"Входные данные"
		with st.container():
			grid = make_grid(4, (2, 2, 8))
			if self.gsop:
				label_list = ["Колличество Этажей", "Общая площадь здания"]
				self._create_labels(label_list,grid)
				self.gsop_data = self.gsop
				flor_widget = grid[1][1].number_input(
        "Введите Колличество Этажей", 
        min_value=2, 
        value=2,
				                                      label_visibility="collapsed"
                                          )
				self.building_area = grid[2][1].number_input(
        "Введите  Общую площадь здания",
        min_value=1, 
        value=1000,
				                                             label_visibility="collapsed")
				self.level_number = 12 if flor_widget >= 12 else flor_widget
			
			else:
				label_list = ["ГСОП", "Колличество Этажей", "Общая площадь здания"]
				self._create_labels(label_list, grid)
				gsop_widget =grid[1][1].number_input("Введите ГСОП", min_value=2000, value=2000,label_visibility="collapsed")
				self.gsop_data = gsop_widget
				flor_widget = grid[2][1].number_input("Введите Колличество Этажей", 
                                          min_value=2, 
                                          value=2,
				                                      label_visibility="collapsed")
				self.building_area = grid[3][1].number_input(
        "Введите  Общую площадь здания", 
        min_value=1, 
        value=1000,
				                                             label_visibility="collapsed")
				self.level_number = 12 if flor_widget >= 12 else flor_widget
		
	def _create_result_chart(self):
		"Результаты"
		st.subheader("Результаты расчетов")
		tab = st.tabs(["Энергопотери МКД","Диаграмма энергопотерь","Справочная информация"])
		df_values = self.add_energy_class_by_building_volume()
		fig = px.bar(df_values,
			             x=self.bar_x,
			             y=self.bar_total_energy_y,
			             color=self.bar_color
			             )
		with tab[0]:
			self._create_metrics(df_values)
			self._local_presents_compare(df_values)
			st.markdown("""##### Энергетические годовые потери энергии  кВт/ч""")
			st.write(df_values)
			st.write(f"""
			Примичание:\n 
   количество газа в 1 кВт теплопотерь МКД- {Constant.kwt_to_m_3.value} м3/кВт,\n 
   стоимость 1 м3 газа {Constant.gas_coast.value} руб/м3,\n 
   выделение С02 из природного газа {Constant.co2_const.value} кг/м3""")
		with tab[1]:
			st.markdown("##### Диаграмма сравнения годовых потерь энергии кВт/ч")
			st.markdown(f"""##### при ГСОП {round(self.gsop_data)}  колличестве этажей  {self.level_number}	 общей площади {self.building_area} м2""" )
			
			st.write(fig)
		with tab[2]:
			self._create_local_heat_tab(self.input_data_frame)
			
	@staticmethod
	def _create_labels(label_list,grid):
		for en, label in enumerate(label_list, start=1):
			grid[en][0].write(label)

	def _create_metrics(self,df_values:pd.DataFrame):
		col_combobox = st.columns([2, 2, 3])
		self.energy_class1 = col_combobox[0].selectbox("Выберите класс Энергоэффективности 1",
		                                               options=ClASS_DATA.keys(), key="energy_class1")
		self.energy_class2 = col_combobox[1].selectbox("Выберите класс Энергоэффективности 2",
		                                               options=ClASS_DATA.keys(), key="energy_class2")
		gas_metrics = self.gas_metrics(df_values, self.energy_class1, self.energy_class2)
		col_combobox[0].metric(
			label=f"Стоимость газа класс {self.energy_class1}", value=f"{gas_metrics.coast_gas_class_1:,.0f}")
		col_combobox[1].metric(
			label=f"Стоимость газа класс {self.energy_class2}", value=f"{gas_metrics.coast_gas_class_2:,.0f}",
			delta=f"{gas_metrics.delta_coast_gas:,.0f}")
		with col_combobox[2]:
			with elements("gas_metric"):
				with mui.Paper(
						sx={
							"bgcolor": "background.paper",
							"boxShadow": 1,
							"borderRadius": 2,
							"p": 2,
							"minWidth": 500,
							
						}):
					mui.Box(
						f"Разница между  классом  {self.energy_class1} и классом {self.energy_class2}",
						sx={"color": 'text.primary', "fontSize": 24, "fontWeight": 'bold'}
						)
					mui.Box(
						f"расход газа {gas_metrics.delta_consumption_gas:,.0f} м3/год.",
						sx={"color": 'red', "fontSize": 36, "fontWeight": 'medium'}
						)
					mui.Box(
						f"стоимость газа {gas_metrics.delta_coast_gas:,.0f} руб/год.",
						sx={"color": 'green', "fontSize": 36, "fontWeight": 'medium'}
						)
		
	def _create_local_heat_tab(self, df_renamed):
		"Удельные показатели"
		df_values = self.add_energy_class_df_values()
		fig = px.bar(df_values,
		             x=self.bar_x,
		             y=self.bar_y,
		             color=self.bar_color
		             )
		col =st.columns([3,2])

		st.markdown(f"##### Удельные показатели  при ГСОП {round(self.gsop_data)} и колличестве этажей  {self.level_number} без учета площади здания ")
		st.write(df_values)
		st.write(
			"Примечание: данные получены из Таблицы 2  Базовый уровень удельного годового расхода	энергетических ресурсов кВт·ч/м2")
		show_more = st.button("Показать Таблицу 2")
		if show_more:
			self.__create_help_base_table2(df_renamed)
			if self.close:
				st.empty()
				
		# self._create_modal_table1(show_more, df_renamed)
		st.markdown(
			"""##### Диаграма1 распределения удельных энергетических потерь здания согласно классу энергоэффективности """)
		st.write(fig)

	def _create_coast_presents_compare_table(self,df_values):
		st.markdown("""##### Процентный прирост стоимости газа по отношению к базовому значению """)
		df_local = self._coast_presents_compare(df_values)
		st.write(df_local)

	def _create_modal_table1(self, modal_button, df_renamed):
		modal = Modal("Таблица 2", key="Таблица 2 модальное окно")
		if modal_button:
			modal.open()
		if modal.is_open():
			with modal.container():
				self.__create_help_base_table2(df_renamed)

	def __create_help_base_table2(self, df_renamed):
		self.close =st.button("Закрть Таблицу 2")
		st.markdown(
			"""##### Таблица2 Базовый уровень удельного годового расхода энергетических ресурсов кВт·ч/м2 """)  # noqa: E501
		st.write(df_renamed)
		st.write("""
				примечание: Приказ  от 6 июня 2016 года N 399/пр Таблица N 1 
				Правила определения класса энергетической эффективности  многоквартирных домов
				Базовый уровень удельного годового расхода энергетических ресурсов в многоквартирном доме, отражающий
				суммарный удельный годовой расход тепловой энергии на отопление, вентиляцию, горячее водоснабжение, 
				а также на общедомовые нужды
						""")  # noqa: E501
	
	def __separate_thousands(self,number_value):
		value = dict(value=locale.format_string('%.0f', number_value, grouping=True, monetary=True))
		return value
		
	
