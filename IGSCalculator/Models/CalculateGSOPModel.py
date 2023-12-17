import pandas as pd

from IGSCalculator.Models.ClimateData import ClimateData
from Utils.Calculation import _filter_df
from GSOPCalculator.Static.GSOPNamesStatic import GSOPNamesStatic


class CalculateGSOPModel:
	def __init__(self, climate_df: pd.DataFrame, city: str):
		_city_data = _filter_df(climate_df, GSOPNamesStatic.city, city)
		self.city_property = ClimateData(
			t_out_max=_city_data[GSOPNamesStatic.t_out].values[0],
			t_ot_middle=_city_data[GSOPNamesStatic.t_ot_per].values[0],
			z_ot=_city_data[GSOPNamesStatic.z_ot_per].values[0],
			air_velocity_middle=4,
			air_velocity_max=5
		)
