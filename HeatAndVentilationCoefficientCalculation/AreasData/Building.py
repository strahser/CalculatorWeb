from dataclasses import dataclass, field
from HeatAndVentilationCoefficientCalculation.AreasData.Room import Room
from HeatAndVentilationCoefficientCalculation.GeometryData.StructuresData import StructureBase
from HeatAndVentilationCoefficientCalculation.StaticData import CheckConditions
from HeatAndVentilationCoefficientCalculation.StaticData.StaticCoefficientAdditionHeat import \
	StaticCoefficientAdditionHeat
from HeatAndVentilationCoefficientCalculation.StaticData.StaticCoefficientHeatTransmission import \
	StaticCoefficientHeatTransmission
from IGSCalculator.Models.ClimateData import ClimateData
from Utils.RenderModel import RenderModel, RenderModelList


@dataclass()
class Building:
	building_name:str
	climate_data: ClimateData
	building_temperature: float
	heated_volume: float
	level_number: int
	level_height: float
	rooms: [Room]
	all_structures: [StructureBase] = field(default_factory=list)

	def __post_init__(self) -> None:
		for room in self.rooms:
			room.update_room_temperature_coefficient(t_ot_middle=self.climate_data.t_ot_middle,
			                                         t_in_building=self.building_temperature)
			for structure in room.structures_list:
				structure.gsop = self.climate_data.GSOP
				self.all_structures.append(structure)

	def get_building_total_structure_area(self) -> RenderModelList:
		"""общая площадь наружных конструкций здания"""
		output_value = sum([room.structures.get_total_structure_area().output_value for room in self.rooms])
		output_render_value = [room.structures.get_total_structure_area() for room in self.rooms]
		return RenderModelList(render_name="сумма наружных поврехностей ограждения здания",
		                       output_value=output_value,
		                       output_render_list=output_render_value,
		                       key="building_total_structure_area")

	def get_building_structure_heat_resistence_total_coefficient(self) -> float:
		"""общий коэффициент теплопередачи здания"""
		return sum(
			[room.structures.get_structure_heat_resistence_total_coefficient().output_value for room in self.rooms])

	def get_normativ_building_structure_heat_resistence_total_coefficient(self) -> RenderModel:
		"""общий коэффициент теплопередачи здания"""
		return CheckConditions.k_total_norm(self.climate_data.GSOP, self.heated_volume)

	def get_building_compact_coefficient(self) -> float:
		"""коэффициент компактности здания"""
		k_comp = self.get_building_total_structure_area().output_value / self.heated_volume
		check_compact = CheckConditions.check_k_comp_value(k_comp, self.level_number)
		return k_comp

	def get_building_structure_heat_resistence_total_coefficient_local(self) -> RenderModelList:
		"""Удельная теплозащитная характеристика здания"""
		output_value = sum(
			[room.get_structure_heat_resistence_total_coefficient_local().output_value
			 for room in self.rooms]) / self.heated_volume
		output_render_value = [room.get_structure_heat_resistence_total_coefficient_local() for room in
		                       self.rooms]
		return RenderModelList(render_name="Удельная теплозащитная характеристика здания",
		                       output_value=output_value,
		                       output_render_list=output_render_value,
		                       key="building_structure_heat_resistence_total_coefficient_local")

	def get_building_sun_radiation_coefficient(self, sun_radiation_data: dict[str, int]) -> float:
		"""Удельная характеристика теплопоступлений в здании от солнечной радиации вт/м3*c"""
		radiation_sum = sum(
			[room.get_room_sun_radiation_coefficient(sun_radiation_data).output_value for room in self.rooms])
		return 11.6 * radiation_sum / (self.climate_data.GSOP * self.heated_volume)

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
		v = StaticCoefficientHeatTransmission.heat_inertia_coefficient(self.climate_data.GSOP)
		z = StaticCoefficientHeatTransmission.z_0_95
		q_addition_heat = v * z * (k_domestic + k_radiation)
		q_heat = (k_structure.output_value + k_vent - q_addition_heat) * (
				1 - 0.1) * StaticCoefficientAdditionHeat.b_h_1_1_3
		return q_heat
