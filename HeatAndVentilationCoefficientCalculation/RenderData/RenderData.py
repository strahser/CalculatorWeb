import pandas as pd
from HeatAndVentilationCoefficientCalculation.AreasData.Building import Building
from HeatAndVentilationCoefficientCalculation.HeatCalculation.SunRadiationHeat import SunRadiationData


def render_data(building: Building):
	filter_columns = ['name', '_n_temperature_coefficient', 'area', 'R_real', 'a_r_n', 'percent_a_r_n']
	df = pd.DataFrame(building.all_structures)
	df['a_r_n'] = df['_n_temperature_coefficient'] * df['area'] / df['R_real']
	df['percent_a_r_n'] = 100 * df['a_r_n'] / df['a_r_n'].sum()
	df.loc['total'] = df[['area', 'a_r_n', 'percent_a_r_n']].sum()
	df.at[df.index[-1], 'name'] = "Total"
	df = df.fillna("").round(2)
	df_group = df.groupby("label")['percent_a_r_n'].agg(sum).reset_index()
	df_group = df_group[df_group["label"] != ""].round(2)
	df = df[filter_columns]
	short_context = dict(
		k_total_normative_render=building.get_normativ_building_structure_heat_resistence_total_coefficient().output_render_value,
		t_out_max=building.climate_data.t_out_max,
		t_in=building.climate_data.t_in,
		t_ot_middle=building.climate_data.t_ot_middle,
		z_ot=building.climate_data.z_ot,
		GSOP=building.climate_data.GSOP,
		k_total=building.get_building_structure_heat_resistence_total_coefficient_local().output_value,
		k_total_normative=building.get_normativ_building_structure_heat_resistence_total_coefficient().output_value,
		k_sun_radiation_coefficient=building.get_building_sun_radiation_coefficient(SunRadiationData),
		k_building_ventilation_coefficient=building.get_building_ventilation_coefficient(),
		k_building_domestic_heat_coefficient=building.get_building_domestic_heat_coefficient(),
		k_building_local_heating_and_ventilation_coefficient=building.
		get_building_local_heating_and_ventilation_coefficient(SunRadiationData),
		df=df, df_group=df_group
	)
	return {k: round(v, 2) for k, v in short_context.items()}
