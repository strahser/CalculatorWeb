from dataclasses import dataclass
import numpy as np
from HeatAndVentilationCoefficientCalculation.StaticData import StaticCoefficientStructures


@dataclass()
class StructureBase:
	name: str
	area: float
	R_real: float  # фактическиое термическое сопративление
	R_norm: float = None
	gsop: float = None
	orientation: str = None
	short_name: str = ""
	label: str = ""
	_n_temperature_coefficient: float = 1

	def __post_init__(self):
		# self.a_r_n = round(self.get_structure_temperature_heat_coefficient_local(),2)
		self.get_norm_terminal_resistence()

	def get_norm_terminal_resistence(self) -> None:
		self.R_norm = 0

	@property
	def n_temperature_coefficient(self):
		return self._n_temperature_coefficient

	@n_temperature_coefficient.setter
	def n_temperature_coefficient(self, value):
		self._n_temperature_coefficient = value

	def class_name(self):
		return type(self).__name__

	def get_structure_temperature_heat_coefficient_local(self) -> float:
		"""коэффициент теплоперадачи приведенный
        """
		return self.n_temperature_coefficient * (self.area / self.R_real)


@dataclass()
class Wall(StructureBase):
	label: str = "Стена"

	def get_norm_terminal_resistence(self) -> None:
		if self.gsop:
			self.R_norm = 0.00035 * self.gsop + 1.4  # Стен, включая стены в грунте


@dataclass()
class Door(StructureBase):
	label: str = "Дверь"

	def get_norm_terminal_resistence(self) -> None:
		if self.gsop:
			R_norm_wall: float = 0.00035 * self.gsop + 1.4  # Стен, включая стены в грунте
			self.R_norm = 0.55 * R_norm_wall  #


@dataclass()
class Window(StructureBase):
	label: str = "Окно"

	def get_norm_terminal_resistence(self) -> None:
		if self.gsop:
			self.R_norm = np.interp(self.gsop, StaticCoefficientStructures.normal_window_gsop_base,
			                        StaticCoefficientStructures.normal_thermal_coefficient_window_base)  # Фасадных окон


@dataclass()
class Floor(StructureBase):
	# Покрытий и перекрытий над проездами
	label: str = "Перекрытие"

	def get_norm_terminal_resistence(self) -> None:
		if self.gsop:
			self.R_norm = 0.0005 * self.gsop + 2.2


@dataclass()
class Roof(StructureBase):
	# Перекрытий чердачных, над неотапливаемыми подпольями и подвалами
	label: str = "Кровля"

	def get_norm_terminal_resistence(self) -> None:
		if self.gsop:
			self.R_norm = 0.00045 * self.gsop + 1.9


@dataclass()
class Skylight(StructureBase):
	# -Зенитных фонарей
	label: str = "Зенитный фонарь"

	def get_norm_terminal_resistence(self) -> None:
		if self.gsop:
			self.R_norm = 0.000025 * self.gsop + 0.25