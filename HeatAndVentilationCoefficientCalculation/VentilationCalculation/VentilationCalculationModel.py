from dataclasses import dataclass
from HeatAndVentilationCoefficientCalculation.GeometryData.RoomInterfece import RoomI
from HeatAndVentilationCoefficientCalculation.VentilationCalculation.RoomAirExchange import RoomVentilation
from HeatAndVentilationCoefficientCalculation.VentilationCalculation.WindowInfiltration import WindowInfiltration
from HeatAndVentilationCoefficientCalculation.ProjectData.ClimateDataModel import ClimateDataModel
from HeatAndVentilationCoefficientCalculation.VentilationCalculation.VentilationCalculationUtility import air_viscosity


@dataclass()
class VentilationData:
	"""
	floor_area_living для жилых зданий - площадь жилых помещений ( ), к которым относятся спальни,
	детские, гостиные, кабинеты, библиотеки, столовые, кухни-столовые;
	floor_area_heated определяемая согласно СП 117.13330 как сумма площадей всех помещений,
	за исключением коридоров, тамбуров, переходов, лестничных клеток, лифтовых шахт,
	внутренних открытых лестниц и пандусов,
	а также помещений, предназначенных для размещения инженерного оборудования и сетей;
	"""
	room: RoomI
	_climate_data: ClimateDataModel
	_level_height: float
	_level_number: int
	_building_heated_volume: float
	_building_height: float = 0

	@property
	def building_height(self):
		if self._building_height:
			return self._building_height
		if self._level_number:
			return self._level_height * self._level_number
		else:
			return 0

	@building_height.setter
	def building_height(self, value):
		_building_height = value

	def g_inf(self) -> float:
		"""инфильтрация"""
		infiltration = WindowInfiltration(self.building_height,
		                                  self._climate_data.t_ot_middle,
		                                  self._climate_data.t_in,
		                                  self._climate_data.air_velocity_middle)
		g_window = infiltration.g_inf_window(self.room.window_area).output_value
		g_door = infiltration.g_inf_doors(self.room.door_area).output_value
		return g_window + g_door

	def room_ventilation_data(self) -> RoomVentilation:
		""" воздухообмен на человека (общее на здание)"""
		room_ventilation = RoomVentilation(self.room.floor_area_heated,
		                                   self.room.floor_area_living,
		                                   self.room.human_number,
		                                   self._level_height)
		return room_ventilation

	def max_air_change(self):
		return self.room_ventilation_data().max_air_change().output_value

	def n_vent(self, ventilation_working_time: int = 168):
		""""
		Средняя кратность воздухообмена жилой части здания за отопительный период
		"""
		# veintilation_working_time число часов работы механической вентиляции в течение недели;
		time_working_ke = ventilation_working_time / 168
		_g_inf_viscosity = self.g_inf() * time_working_ke / air_viscosity(self._climate_data.t_ot_middle)
		n_vent = (self.max_air_change() * time_working_ke + _g_inf_viscosity) / (
				0.85 * self._building_heated_volume)
		return n_vent

	def get_building_local_ventilation_coefficient(self, k_ef_recuperation=1, ventilation_working_time: int = 168):
		""""
		Удельная вентиляционная характеристика здания
		"""
		k_vent = 0.28 * 1 * self.n_vent(ventilation_working_time) * 0.85 * air_viscosity(
			self._climate_data.t_ot_middle) * k_ef_recuperation
		return k_vent
