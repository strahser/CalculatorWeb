from dataclasses import dataclass, field
from HeatAndVentilationCoefficientCalculation.GeometryData.BaseStructureDataModel import BaseStructureDataModel
from HeatAndVentilationCoefficientCalculation.HeatCalculation.StructureThermalResistenceCoefficient import \
	get_normative_thermal_resistence_coefficient


@dataclass()
class StructureDataModel:
	name: str
	area: float
	base_structures: BaseStructureDataModel
	orientation: str = ""
	short_name: str = ""

	def __post_init__(self):
		self._n_temperature_coefficient = 0

	@property
	def R_real(self):
		return self.base_structures.R_real

	@property
	def standard_structure_type(self):
		return self.base_structures.standard_structure_type

	@property
	def n_temperature_coefficient(self):
		return self._n_temperature_coefficient

	@n_temperature_coefficient.setter
	def n_temperature_coefficient(self, value):
		self._n_temperature_coefficient = value

	@property
	def class_name(self):
		"""для выбора конструкции по названию класса"""
		return type(self).__name__

	def get_structure_temperature_heat_coefficient_local(self, n_temperature_coefficient) -> float:
		"""коэффициент теплоперадачи приведенный
        """
		return n_temperature_coefficient * (self.area / self.R_real)

	def get_normative_terminal_resistence(self, gsop: float) -> float:
		"""перерасчет коэффицинета ГСОП в зависимости от расчетной темпертуры в помещении,
        если она отличается от температуры принятой при расчете ГСОП"""
		return get_normative_thermal_resistence_coefficient(gsop).get(self.standard_structure_type.name)
