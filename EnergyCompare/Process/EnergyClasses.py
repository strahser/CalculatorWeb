import numpy as np
import streamlit
from dataclasses import dataclass
import pandas as pd

from EnergyCompare.Models.EnergyModels import ClASS_DATA, BaseNames,Constant
from EnergyCompare.Process.DataTableInterpolation import DataTableInterpolation

@dataclass
class GasCoastValue:
	coast_gas_class_1:float# при классе эн.эфф1
	coast_gas_class_2: float# при классе эн.эфф2
	delta_coast_gas: float
	delta_consumption_gas: float
	
	


@dataclass
class EnergyClasses:
	energy_class_data: pd.DataFrame
	gsop_data: float
	level_number: int
	building_area:float
	energy_class1:str
	bar_color: str = BaseNames.energy_class.value
	bar_x: str = BaseNames.energy_class.value
	bar_y: str = BaseNames.base_value.value
	bar_total_energy_y: str = BaseNames.total_energy.value

	def __init__(self, input_data_frame: pd.DataFrame):
		self.input_data_frame = input_data_frame
  
	@property
	def interpolate_df_data(self)->pd.DataFrame:
		interpolate_df = DataTableInterpolation(self.input_data_frame)
		interpolate_df_data = interpolate_df.interpolate_df(self.gsop_data, self.level_number)
		return interpolate_df_data

	def add_energy_class_df_values(self) -> pd.DataFrame:
		interpolate_df_data = self.interpolate_df_data.copy()
		for col, val in ClASS_DATA.items():
			interpolate_df_data[col] = interpolate_df_data[BaseNames.base_name.value] * val
		return interpolate_df_data.melt(var_name=BaseNames.energy_class.value,
										value_name=BaseNames.base_value.value)

	def add_energy_class_by_building_volume(self)->pd.DataFrame:
		interpolate_df_data = self.interpolate_df_data.copy()
		for col, val in ClASS_DATA.items():
			interpolate_df_data[col] = interpolate_df_data[BaseNames.base_name.value] * val*self.building_area
		interpolate_df_data = interpolate_df_data\
			.drop(columns =BaseNames.base_name.value)\
			.melt(var_name=BaseNames.energy_class.value,value_name=BaseNames.total_energy.value)
		interpolate_df_data["Расход газа, м3"] =interpolate_df_data[BaseNames.total_energy.value]*Constant.kwt_to_m_3.value
		interpolate_df_data["Стоимость газа,руб"] = interpolate_df_data[BaseNames.total_energy.value] * Constant.gas_coast.value
		interpolate_df_data["выделение С02 кг"] = interpolate_df_data["Расход газа, м3"] * Constant.co2_const.value
		interpolate_df_data["стоимость С02 руб"] = interpolate_df_data["выделение С02 кг"] * Constant.co2_coast.value
		return interpolate_df_data

	def gas_metrics(self,df_values:pd.DataFrame,energy_class1,energy_class2):
		def __sub_query(value,returned_column_value):
			return df_values[df_values[BaseNames.energy_class.value] == value][returned_column_value].values[0]
			
		coast_class_1=__sub_query(energy_class1,"Стоимость газа,руб")
		coast_class_2 = __sub_query(energy_class2,"Стоимость газа,руб")
		delta_cost = coast_class_2-coast_class_1
		delta_consumption_gas = __sub_query(energy_class2,"Расход газа, м3")-__sub_query(energy_class1,"Расход газа, м3")
		gas_coast = GasCoastValue(coast_class_1,coast_class_2,delta_cost,delta_consumption_gas)
		return gas_coast
		
	def _coast_presents_compare(self, df:pd.DataFrame)->pd.DataFrame:
		df["процентный прирост"] = df[BaseNames.base_value.value]\
			.pct_change()\
			.cumsum().mul(100).round()
		df = df.filter([BaseNames.energy_class.value,"процентный прирост"])
		return df


	def _local_presents_compare(self, df:pd.DataFrame)->pd.DataFrame:
		value_comp = df[df[BaseNames.energy_class.value] == self.energy_class1]["Стоимость газа,руб"].values[0]
		new_name = f"процентный прирост класс {self.energy_class1}"
		df[new_name] = df["Стоимость газа,руб"]/value_comp
		df = df.filter([BaseNames.energy_class.value, new_name])
		return df

	@staticmethod
	def __transform_df(df):
		df = df.T
		df.columns = df.iloc[0]
		df = df.reset_index().rename(columns={"index": BaseNames.energy_class.value}).iloc[1:, :]
		return df