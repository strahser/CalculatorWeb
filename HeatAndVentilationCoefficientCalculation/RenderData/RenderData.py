import pandas as pd
from HeatAndVentilationCoefficientCalculation.SpaceData.BuildingDataModel import BuildingDataModel
from HeatAndVentilationCoefficientCalculation.StaticData.OrientationData import OrientationData
from HeatAndVentilationCoefficientCalculation.StaticData.StructureTypeData import StructureTypeData
from HeatAndVentilationCoefficientCalculation.StaticData.SunRadiationHeat import SunRadiationHeat
from typing import Any, List
from pytexit import py2tex


def render_data(building: BuildingDataModel) -> dict[str, Any]:
    def _create_additional_df_columns(column_name: str) -> List[List[Any]]:
        """из всех  помещений здания забираем листы конструкций"""
        return [[getattr(val, column_name) for val in room.structures_list] for room in building.rooms][0]

    def create_df_from_structure_data(additional_columns: List[str]) -> pd.DataFrame:
        """Определяем приведенный коэффициент теплоперадчи и распределение тепла через каждый тип конструкции"""
        df = pd.DataFrame([room.structures_list for room in building.rooms][0])
        for col_name in additional_columns:
            df[col_name] = _create_additional_df_columns(col_name)
        df['a_r_n'] = df['n_temperature_coefficient'] * df['area'] / df['R_real']
        df['percent_a_r_n'] = 100 * df['a_r_n'] / df['a_r_n'].sum()
        df.loc['total'] = df[['area', 'a_r_n', 'percent_a_r_n']].sum()
        df.at[df.index[-1], 'name'] = "Итого"
        df = df.fillna("").round(2)
        return df

    def create_structure_data_frame() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """группируем конструкции по типу, агрегируем по % доле каждой групп конструкций"""
        additional_df_column = ['standard_structure_type', 'R_real', 'n_temperature_coefficient']
        filter_columns = ['name', 'n_temperature_coefficient', 'area', 'R_real', 'a_r_n', 'percent_a_r_n']
        building.update_room_coefficient()
        df = create_df_from_structure_data(additional_df_column)
        df_group = df.groupby("standard_structure_type")['percent_a_r_n'].agg(sum).reset_index()
        df_group = df_group[df_group["standard_structure_type"] != ""].round(2)  # получаем Door,Wall...данные
        df_group = df_group.replace({i.name: i.value for i in StructureTypeData})
        df_window_group = df.query("standard_structure_type =='Window'").groupby("orientation")['area'] \
            .agg(sum).reset_index().replace({val.name: val.value for val in OrientationData})
        return df[filter_columns], df_group, df_window_group

    def create_short_dictionary() -> dict[str, Any]:
        df, df_group, df_window_group = create_structure_data_frame()
        k_total_normative = building.get_normative_building_structure_heat_resistence_total_coefficient()
        short_context = dict(
            k_total_normative_render=py2tex(k_total_normative.output_render_value.replace('=', '==')),
            t_out_max=building.climate_data.t_out_max,
            t_in=building.building_temperature,
            t_ot_middle=building.climate_data.t_ot_middle,
            z_ot=building.climate_data.z_ot,
            GSOP=building.GSOP,
            k_total=building.get_building_structure_heat_resistence_total_coefficient_local().output_value,
            k_total_normative=building.get_normative_building_structure_heat_resistence_total_coefficient().output_value,
            k_sun_radiation_coefficient=building.get_building_sun_radiation_coefficient(SunRadiationHeat),
            k_building_ventilation_coefficient=building.get_building_ventilation_coefficient(),
            k_building_domestic_heat_coefficient=building.get_building_domestic_heat_coefficient(),
            k_building_local_heating_and_ventilation_coefficient=building.
            get_building_local_heating_and_ventilation_coefficient(SunRadiationHeat),
            df=df, df_group=df_group, df_window_group=df_window_group
        )
        return short_context

    def reorder_dictionary():
        short_context = create_short_dictionary()
        temp_dict = {}
        for k, v in short_context.items():
            try:
                temp_dict[k] = round(v, 2)
            except:
                temp_dict[k] = v
        return temp_dict

    return reorder_dictionary()
