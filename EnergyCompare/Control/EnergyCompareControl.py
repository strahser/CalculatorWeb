
import pandas as pd
from EnergyCompare.Models.EnergyModels import BaseNames
from EnergyCompare.Views.EnergyView import EnergyView


def rename_numerical_column_to_index_string(df, num_column: int, new_name: str) -> pd.DataFrame:  # noqa: E501
	return df.rename({num_column: new_name}, axis=1).set_index(new_name)


def energy_compare_control(input_data_frame:pd.DataFrame,gsop):
	df_renamed = rename_numerical_column_to_index_string(input_data_frame, 0, BaseNames.gsop.value)  # noqa: E501
	energy_view = EnergyView(input_data_frame=input_data_frame,gsop=gsop)
	energy_view.create_tabs()

