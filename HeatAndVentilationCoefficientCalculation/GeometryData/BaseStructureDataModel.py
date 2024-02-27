from dataclasses import dataclass, field
from HeatAndVentilationCoefficientCalculation.HeatCalculation.StructureThermalResistenceCoefficient import \
	get_normative_thermal_resistence_coefficient
from HeatAndVentilationCoefficientCalculation.StaticData.StructureTypeData import StructureTypeData


@dataclass()
class BaseStructureDataModel:
	R_real: float  # фактическиое термическое сопративление
	standard_structure_type: str
	name: str=""
