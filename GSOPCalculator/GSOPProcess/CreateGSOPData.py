
import pandas as pd
from dataclasses import dataclass, field
from EnergyCompare.Utility.PandasFunctions import load_input_data_frame
from GSOPCalculator.Static.GSOPNamesStatic import GSOPNamesStatic


@dataclass		
class CityProperty:
	t_out:float
	t_ot_per:float
	z_ot_per:float

@dataclass		
class BuildingProperty:
	t_in:float

@dataclass		
class GsopData:
	gsop_value:float
	gsop_str:str

@dataclass
class CalculateGSOP:
	original_df: pd.DataFrame
	selected_region: str = field(init=False)
	selected_city: str = field(init=False)
	
	
	@property
	def building_property(self,t_in=20):
		_building_property = BuildingProperty(t_in)
		return _building_property
		
	
	@property
	def city_property(self):
		city = self._filter_df(self.df, GSOPNamesStatic.city, self.selected_city)
		_city_property =CityProperty(
		city[GSOPNamesStatic.t_out].values[0] ,
		city[GSOPNamesStatic.t_ot_per].values[0],
		city[GSOPNamesStatic.z_ot_per].values[0]
		)
		return _city_property
	
	@property
	def gsop(self):
		_city = self.city_property
		_gsop = (self.building_property.t_in - self.city_property.t_ot_per) * self.city_property.z_ot_per
		_gsop_str = f"({self.building_property.t_in} - {self.city_property.t_ot_per}) * {self.city_property.z_ot_per} = {_gsop}"
		_gsop_data =GsopData(_gsop,_gsop_str)
		return _gsop_data
	
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
	

		

	
	
	
