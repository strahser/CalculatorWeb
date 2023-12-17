from dataclasses import dataclass, field
import numpy as np
from HeatAndVentilationCoefficientCalculation.StaticData.StaticCoefficientStructures import StaticCoefficientStructures
from Utils.RenderModel import RenderModel


@dataclass()
class Structure:
	name: str
	area: float
	R_real: float  # фактическиое термическое сопративление
	R_norm: float = field(init=False)
	gsop: float
	orientation: str = None
	short_name: str = ""
	_n_temperature_koef: float = 1
	a_r_n: float = field(init=False)  # self.n_temperature_koef * (self.area / self.R_real)
	percent_a_r_n: float = 0

	def __post_init__(self):
		self.a_r_n = round(self.get_structure_temperature_heat_coefficient_local(),1)
		self.get_norm_terminal_resistence()

	def get_norm_terminal_resistence(self) -> None:
		self.R_norm = 0

	@property
	def n_temperature_koef(self):
		return self._n_temperature_koef

	@n_temperature_koef.setter
	def n_temperature_koef(self, value):
		self._n_temperature_koef = value

	def class_name(self):
		return type(self).__name__

	def get_structure_temperature_heat_coefficient_local(self) -> float:
		"""коэффициент теплоперадачи приведенный
        """
		return self.n_temperature_koef * (self.area / self.R_real)


@dataclass()
class Wall(Structure):

	def get_norm_terminal_resistence(self) -> None:
		self.R_norm = 0.00035 * self.gsop + 1.4  # Стен, включая стены в грунте


@dataclass()
class Door(Structure):

	def get_norm_terminal_resistence(self) -> None:
		if self.gsop:
			R_norm_wall: float = 0.00035 * self.gsop + 1.4  # Стен, включая стены в грунте
			self.R_norm = 0.55 * R_norm_wall  #


@dataclass()
class Window(Structure):
	def get_norm_terminal_resistence(self) -> None:
		if self.gsop:
			self.R_norm = np.interp(self.gsop, StaticCoefficientStructures.normal_window_gsop_base,
			                        StaticCoefficientStructures.normal_thermal_coefficient_window_base)  # Фасадных окон


@dataclass()
class Floor(Structure):
	# Покрытий и перекрытий над проездами

	def get_norm_terminal_resistence(self) -> None:
		if self.gsop:
			self.R_norm = 0.0005 * self.gsop + 2.2


@dataclass()
class Roof(Structure):
	# Перекрытий чердачных, над неотапливаемыми подпольями и подвалами

	def get_norm_terminal_resistence(self) -> None:
		if self.gsop:
			self.R_norm = 0.00045 * self.gsop + 1.9


@dataclass()
class Skylight(Structure):
	# -Зенитных фонарей

	def get_norm_terminal_resistence(self) -> None:
		if self.gsop:
			self.R_norm = 0.000025 * self.gsop + 0.25


@dataclass()
class Structures:
	"""расчитывает теплотехнические коэффициенты всех ограждений помещения"""
	structures_list: list[Structure]

	def get_structure_heat_resistence_total_coefficient(self) -> RenderModel:
		"""общий коэффициент теплопередачи ограждений"""
		output_value = sum(
			[
				structure.get_structure_temperature_heat_coefficient_local()
				for structure in self.structures_list
			]) / self.get_total_structure_area().output_value

		render_list = RenderModel.create_string_list_sum(
			"get_structure_temperature_heat_coefficient_local", self.structures_list)
		output_render_value = f"kоб={render_list}/{self.get_total_structure_area().output_value}={output_value}"
		return RenderModel(render_name="общий коэффициент теплопередачи ограждений",
		                   output_value=output_value,
		                   output_render_value=output_render_value,
		                   key="k_heat_resistence_total")

	def get_structure_heat_resistence_total_coefficient_local(self) -> RenderModel:
		"""суммарный приведенный коэффициент теплопередачи для выбранных ограждений"""
		output_value = sum(
			[structure.get_structure_temperature_heat_coefficient_local() for structure in self.structures_list])
		render_list = RenderModel.create_string_list_sum(
			"get_structure_temperature_heat_coefficient_local", self.structures_list)
		output_render_value = f"ksum={render_list}={output_value}"
		return RenderModel(render_name="суммарный приведенный коэффициент теплопередачи для выбранных ограждений",
		                   output_value=output_value,
		                   output_render_value=output_render_value,
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
