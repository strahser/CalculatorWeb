

from enum import Enum
from HeatAndVentilationCoefficientCalculation.GeometryData.StructuresData import *
from dataclasses import dataclass


@dataclass()
class StructureData:
	structure_name: str
	class_value: object


class StructureTypeData(Enum):
	Wall: str = StructureData("Стена", Wall)
	Door: str = StructureData("Дверь", Door)
	Window: str = StructureData("Окно", Window)
	Skylight: str = StructureData("Зенитный фонарь", Skylight)
	Floor: str = StructureData("Перекрытие", Floor)
	Roof: str = StructureData("Кровля", Roof)
	def get_R(self):
		return {self.Wall.name:""}