
import pandas as pd
from dataclasses import dataclass, field
from EnergyCompare.Utility.PandasFunctions import load_input_data_frame
from GSOPCalculator.Static.GSOPNamesStatic import GSOPNamesStatic


@dataclass
class CalculateGSOP:
	original_df: pd.DataFrame
	selected_region: str = field(init=False)
	selected_city: str = field(init=False)	
	
	@property
	def gsop(self):
		_city = self._filter_df(self.df, GSOPNamesStatic.city, self.selected_city)
		_city = _city.assign(gsop=_city.apply(self.__calculate_gsop_function, axis=1))
		return _city[GSOPNamesStatic.gsop].values[0]
	
	@property
	def unique_city(self) -> list:
		region = self._filter_df(self.df, GSOPNamesStatic.region, self.selected_region)
		return region[GSOPNamesStatic.city].unique()
	
	@property
	def all_regions(self) -> list:
		return self.df[GSOPNamesStatic.region].unique()
	
	@property
	def all_city(self) -> list:
		return self.df[GSOPNamesStatic.city].unique()
	
	@property
	def df(self):
		df =  self.original_df.copy()
		df[GSOPNamesStatic.region] = df[GSOPNamesStatic.region].ffill()
		return df
	
	@staticmethod
	def _filter_df(df: pd.DataFrame, column_name: str, column_value):
		query = df[column_name] == column_value
		return df[query]
	
	@staticmethod
	def __calculate_gsop_function(df,t_in:int =20) -> float:
		return (t_in - df[GSOPNamesStatic.t_ot_per]) * df[GSOPNamesStatic.z_ot_per]