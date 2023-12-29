

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
	Skylight: str = StructureData("Зенитный фанарь", Skylight)
	Floor: str = StructureData("Перекрытие", Floor)
	Roof: str = StructureData("Кровля", Roof)
