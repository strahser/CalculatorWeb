from dataclasses import dataclass
from IGSCalculator.Models.ClimateData import ClimateData
from HeatAndVentilationCoefficientCalculation.GeometryData.RoomInterfece import RoomI
from HeatAndVentilationCoefficientCalculation.GeometryData.StructuresData import Structures, Window, Door
from HeatAndVentilationCoefficientCalculation.HeatCalculation.DomesticHeat import DomesticHeat
from HeatAndVentilationCoefficientCalculation.StaticData.StaticCoefficientStructures import StaticCoefficientStructures
from HeatAndVentilationCoefficientCalculation.VentilationCalculation.VentilationCalculationModel import VentilationData
from Utils.RenderModel import RenderModel


@dataclass()
class Room(RoomI):
	structures: Structures
	category: str
	human_number: int = 1
	t_in_room: float = 20  # температуры в помещениях
	t_in_building: float = 20  # расчетная внутренняя температура здания
	t_ot: float = None  # средняя температура в отопительный период.
	room_heated_volume: float = None  # отапливаемый объем помещения
	floor_area_living: float = 0  # жилые помещения для МКД
	floor_area_heated: float = 0  # отапливаемые помещения для МКД

	def __post_init__(self) -> None:
		""" если не заданы отапливаемые площади или жилые площади, то приравниваем известные площади здания к
			Отапливаемым. Выделяем площади дверей и окон.
		"""
		self.floor_area_heated = self.floor_area_living if self.floor_area_heated == 0 else self.floor_area_heated
		self.floor_area_living = self.floor_area_heated if self.floor_area_living == 0 else self.floor_area_living
		self.windows = [val for val in self.structures.structures_list if val.__class__.__name__ == Window.__name__]
		self._door_area = None
		self._window_area = None

	def update_room_temperature_coefficient(self):
		"""Обновляем температурный коэффициент помещения в зависимости от температуры здания (при расчете ГСОП)"""
		if self.t_in_room != self.t_in_building and self.t_ot:
			for structure in self.structures.structures_list:
				structure.n_temperature_koef = StaticCoefficientStructures.temperature_coefficient_n_calculated(
					self.t_ot,
					self.t_in_building,
					self.t_in_room
				)

	@property
	def window_area(self):
		return sum([val.area for val in self.windows])

	@window_area.setter
	def window_area(self, value):
		self._window_area = value

	@property
	def door_area(self):
		return sum([val.area for val in self.structures.structures_list if val.__class__.__name__ == Door.__name__])

	@door_area.setter
	def door_area(self, value):
		self._door_area = value

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
		                   output_render_value=output_render_value,key="Q_radiation_annual")

	def get_room_ventilation_coefficient(self,
	                                     climate_data: ClimateData,
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
