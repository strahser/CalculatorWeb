from dataclasses import dataclass
from typing import List

from HeatAndVentilationCoefficientCalculation.SpaceData.RoomDataModel import RoomDataModel
from HeatAndVentilationCoefficientCalculation.StaticData.BuildingCategory import BuildingCategory
from HeatAndVentilationCoefficientCalculation.StaticData.CheckConditions import CheckConditions
from HeatAndVentilationCoefficientCalculation.StaticData.StaticCoefficientAdditionHeat import \
    StaticCoefficientAdditionHeat
from HeatAndVentilationCoefficientCalculation.StaticData.StaticCoefficientHeatTransmission import \
    StaticCoefficientHeatTransmission
from HeatAndVentilationCoefficientCalculation.ProjectData.ClimateDataModel import ClimateDataModel
from Utils.RenderModel import RenderModel, RenderModelList


@dataclass()
class BuildingDataModel:
    name: str
    category: str
    heated_volume: float
    level_number: int
    level_height: float
    building_temperature: float
    climate_data: ClimateDataModel
    rooms: List[RoomDataModel]

    @property
    def GSOP(self):
        return (self.building_temperature - self.climate_data.t_ot_middle) * self.climate_data.z_ot

    def get_building_total_structure_area(self) -> RenderModelList:
        """общая площадь наружных конструкций здания"""
        total_structure_area = sum([room.get_total_structure_area().output_value for room in self.rooms])
        return RenderModelList(render_name="сумма наружных поврехностей ограждения здания",
                               output_value=total_structure_area,
                               output_render_list=total_structure_area,
                               key=self.get_building_total_structure_area.__name__)

    def update_room_coefficient(self) -> None:
        for room in self.rooms:
            room.update_structure_coefficient(self.climate_data.t_ot_middle, self.building_temperature)

    def get_building_structure_heat_resistence_total_coefficient(self) -> RenderModelList:
        """общий коэффициент теплопередачи здания"""
        _total_coefficient = sum(
            [room.get_structure_heat_resistence_total_coefficient(
                self.climate_data.t_ot_middle, self.building_temperature
            ).output_value for room in self.rooms]
        )
        return RenderModelList(render_name="общий коэффициент теплопередачи здания",
                               output_value=_total_coefficient,
                               output_render_list=_total_coefficient,
                               key=self.get_building_structure_heat_resistence_total_coefficient.__name__)

    def get_normative_building_structure_heat_resistence_total_coefficient(self) -> RenderModel:
        """общий коэффициент теплопередачи здания"""
        return CheckConditions.k_total_norm(self.GSOP, self.heated_volume)

    def get_building_compact_coefficient(self) -> float:
        """коэффициент компактности здания"""
        k_comp = self.get_building_total_structure_area().output_value / self.heated_volume
        check_compact = CheckConditions.check_k_comp_value(k_comp, self.level_number)  # todo add info to frontend
        return k_comp

    def get_building_structure_heat_resistence_total_coefficient_local(self) -> RenderModelList:
        """Удельная теплозащитная характеристика здания"""
        get_structure_coefficient_local = sum(
            [room.get_structure_heat_resistence_total_coefficient_local(
                self.climate_data.t_ot_middle, self.building_temperature).output_value
             for room in self.rooms])
        return RenderModelList(render_name="Удельная теплозащитная характеристика здания",
                               output_value=get_structure_coefficient_local / self.heated_volume,
                               output_render_list=get_structure_coefficient_local / self.heated_volume,
                               key="building_structure_heat_resistence_total_coefficient_local")

    def get_building_sun_radiation_coefficient(self, sun_radiation_data: dict[str, int]) -> float:
        """Удельная характеристика теплопоступлений в здании от солнечной радиации вт/м3*c"""
        radiation_sum = sum(
            [room.get_room_sun_radiation_coefficient(sun_radiation_data).output_value for room in self.rooms])
        return 11.6 * radiation_sum / (self.GSOP * self.heated_volume)

    def get_building_ventilation_coefficient(self) -> float:
        """
        Удельная вентиляционная характеристика здания
        """
        return sum([
            room.get_room_ventilation_coefficient(
                climate_data=self.climate_data,
                level_height=self.level_height,
                level_number=self.level_number,
                building_heated_volume=self.heated_volume,
            )
            for room in self.rooms
        ])

    def get_building_domestic_heat_coefficient(self) -> float:
        """бытовые тепловыделения здания"""
        return sum([
            room.get_room_domestic_heat_coefficient(self.heated_volume, self.climate_data.t_ot_middle).output_value
            for room in self.rooms
        ])

    def get_building_local_heating_and_ventilation_coefficient(self, sun_radiation_data: dict[str, int]) -> float:
        """
        Расчетная удельная характеристика расхода тепловой энергии
        на отопление и вентиляцию здания за отопительный период
        """
        k_structure = self.get_building_structure_heat_resistence_total_coefficient_local()
        k_vent = self.get_building_ventilation_coefficient()
        k_domestic = self.get_building_domestic_heat_coefficient()
        k_radiation = self.get_building_sun_radiation_coefficient(sun_radiation_data)
        v = StaticCoefficientHeatTransmission.heat_inertia_coefficient(self.GSOP)
        z = StaticCoefficientHeatTransmission.z_0_95
        q_addition_heat = v * z * (k_domestic + k_radiation)
        q_heat = (k_structure.output_value + k_vent - q_addition_heat) * (
                1 - 0.1) * StaticCoefficientAdditionHeat.b_h_1_1_3
        return q_heat
