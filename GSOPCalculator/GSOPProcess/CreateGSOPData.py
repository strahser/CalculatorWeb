import pandas as pd
from dataclasses import dataclass, field
from EnergyCompare.Utility.PandasFunctions import load_input_data_frame
from GSOPCalculator.GSOPModel.BuildingProperty import BuildingProperty
from GSOPCalculator.GSOPModel.CityProperty import CityProperty
from Utils.Calculation import _filter_df
from GSOPCalculator.Static.GSOPNamesStatic import GSOPNamesStatic


@dataclass
class CalculateGSOP:
	original_df: pd.DataFrame
	selected_region: str = field(init=False)
	selected_city: str = field(init=False)

	@property
	def building_property(self, t_in=20):
		_building_property = BuildingProperty(t_in)
		return _building_property

	@property
	def city_property(self):
		city = _filter_df(self.df, GSOPNamesStatic.city, self.selected_city)
		_city_property = CityProperty(
			city[GSOPNamesStatic.t_out].values[0],
			city[GSOPNamesStatic.t_ot_per].values[0],
			city[GSOPNamesStatic.z_ot_per].values[0]
		)
		return _city_property

	@property
	def gsop(self):
		_city = self.city_property
		_gsop_data = self.city_property.gsop_value
		return _gsop_data

	@property
	def unique_city(self) -> list:
		region = _filter_df(self.df, GSOPNamesStatic.region, self.selected_region)
		return region[GSOPNamesStatic.city].unique()

	@property
	def all_regions(self) -> list:
		return self.df[GSOPNamesStatic.region].unique()

	@property
	def all_city(self) -> list:
		return self.df[GSOPNamesStatic.city].unique()

	@property
	def df(self):
		df = self.original_df.copy()
		df[GSOPNamesStatic.region] = df[GSOPNamesStatic.region].ffill()
		return df
