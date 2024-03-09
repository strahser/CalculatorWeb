from dataclasses import dataclass, field
from HeatAndVentilationCoefficientCalculation.GeometryData.StructuresDataModel import StructureDataModel
from HeatAndVentilationCoefficientCalculation.StaticData.RoomCategory import RoomCategory
from HeatAndVentilationCoefficientCalculation.StaticData.StructureTypeData import StructureTypeData
from HeatAndVentilationCoefficientCalculation.ProjectData.ClimateDataModel import ClimateDataModel
from HeatAndVentilationCoefficientCalculation.GeometryData.RoomInterfece import RoomI
from HeatAndVentilationCoefficientCalculation.HeatCalculation.DomesticHeat import DomesticHeat
from HeatAndVentilationCoefficientCalculation.StaticData.StaticCoefficientStructures import StaticCoefficientStructures
from HeatAndVentilationCoefficientCalculation.VentilationCalculation.VentilationCalculationModel import VentilationData
from Utils.RenderModel import RenderModel


@dataclass()
class RoomDataModel(RoomI):
	name: str
	structures_list: list[StructureDataModel]
	category: str
	human_number: int = 1
	t_in_room: float = 20  # температуры в помещениях
	room_heated_volume: float = 1  # отапливаемый объем помещения
	floor_area_living: float = 1  # жилые помещения для МКД
	floor_area_heated: float = 1  # отапливаемые помещения для МКД

	def __post_init__(self) -> None:
		""" если не заданы отапливаемые площади или жилые площади, то приравниваем известные площади здания к
			Отапливаемым. Выделяем площади дверей и окон.
		"""
		self.floor_area_heated = self.floor_area_living if self.floor_area_heated == 0 else self.floor_area_heated
		self.floor_area_living = self.floor_area_heated if self.floor_area_living == 0 else self.floor_area_living
		self.windows = [val for val in self.structures_list if
		                val.standard_structure_type == StructureTypeData.Window.name]
		self.doors = [val for val in self.structures_list if val.standard_structure_type == StructureTypeData.Door.name]
		self._window_area = 0
		self._door_area = 0
		self.n_temperature_coefficient = 0

	@property
	def window_area(self):
		return sum([val.area for val in self.windows])

	@window_area.setter
	def window_area(self, value):
		self._window_area = value

	@property
	def door_area(self):
		return sum([val.area for val in self.doors])

	@door_area.setter
	def door_area(self, value):
		self._door_area = value

	def update_structure_coefficient(self, t_ot_middle: float, t_in_building: float):
		for structure in self.structures_list:
			self.n_temperature_coefficient = self.temperature_coefficient_n_calculated(t_ot_middle, t_in_building)
			structure.n_temperature_coefficient = self.n_temperature_coefficient

	def temperature_coefficient_n_calculated(self, t_ot_middle: float, t_in_building: float) -> float:
		"""Обновляем температурный коэффициент помещения в зависимости от температуры здания (при расчете ГСОП)
			t_ot: float   средняя температура в отопительный период.
			t_in_building: float = 20  расчетная внутренняя температура здания
		"""
		return StaticCoefficientStructures.temperature_coefficient_n_calculated(t_ot_middle, t_in_building,
		                                                                        self.t_in_room)

	def get_structure_heat_resistence_total_coefficient(self, t_ot_middle: float, t_in_building: float) -> RenderModel:
		"""общий коэффициент теплопередачи ограждений"""
		output_value = sum(
			[
				structure.get_structure_temperature_heat_coefficient_local(
					self.temperature_coefficient_n_calculated(t_ot_middle, t_in_building))
				for structure in self.structures_list
			]
		) / self.get_total_structure_area().output_value

		return RenderModel(render_name="общий коэффициент теплопередачи ограждений",
		                   output_value=output_value,
		                   output_render_value=str(output_value),
		                   key="k_heat_resistence_total")

	def get_structure_heat_resistence_total_coefficient_local(self, t_ot_middle: float,
	                                                          t_in_building: float) -> RenderModel:
		"""суммарный приведенный коэффициент теплопередачи для выбранных ограждений"""
		output_value = sum(
			[structure.get_structure_temperature_heat_coefficient_local(
				self.temperature_coefficient_n_calculated(t_ot_middle, t_in_building))
				for structure in self.structures_list
			])
		return RenderModel(render_name="суммарный приведенный коэффициент теплопередачи для выбранных ограждений",
		                   output_value=output_value,
		                   output_render_value=str(output_value),
		                   key="structure_heat_resistence_total_coefficient_local")

	def get_total_structure_area(self) -> RenderModel:
		"""сумма наружных поврехностей ограждения"""
		output_value = sum([structure.area for structure in self.structures_list])
		join_list = (str(round(structure.area, 1)) for structure in self.structures_list)
		output_render_value = f"{'+'.join(join_list)} ={output_value}"
		return RenderModel(render_name="сумма наружных поврехностей ограждения",
		                   output_value=output_value,
		                   output_render_value=output_render_value,
		                   key="total_structure_area")

	def get_room_sun_radiation_coefficient(self, sun_radiation_data: dict[str, int]) -> RenderModel:
		"""расчет годовой солнечной радиации комнаты
		sun_radiation_data -словарь со значением солнечной радиации по сторонам света
		"""
		sum_list = sum(
			[sun_radiation_data.get(val.orientation, 0) * val.area for val in self.windows])
		output_value = 0.8 * 0.74 * sum_list
		str_list_sum = "".join(
			[f"{sun_radiation_data.get(val.orientation, 0)} * {val.area}+" for val in self.windows])

		output_render_value = f"0.8 * 0.74 * sum({str_list_sum})= 0.8 * 0.74 * {sum_list} = {output_value}"
		return RenderModel("Солнечная радиация годовая", output_value=output_value,
		                   output_render_value=output_render_value, key="Q_radiation_annual")

	def get_room_ventilation_coefficient(self,
	                                     climate_data: ClimateDataModel,
	                                     level_height,
	                                     level_number,
	                                     building_heated_volume: float):
		"""
		Удельная вентиляционная характеристика помещения
		"""
		ventilation_data = VentilationData(room=self,
		                                   _climate_data=climate_data,
		                                   _level_height=level_height,
		                                   _level_number=level_number,
		                                   _building_heated_volume=building_heated_volume,
		                                   )
		return ventilation_data.get_building_local_ventilation_coefficient()

	def get_room_domestic_heat_coefficient(self, building_heated_volume: float, t_ot_middle):
		"""бытовые тепловыделения помещения"""
		domestic_heat_data = DomesticHeat(_room=self)
		return domestic_heat_data.domestic_heat_coefficient(
			building_heated_volume=building_heated_volume,
			t_in=self.t_in_room,
			t_ot_middle=t_ot_middle
		)
