from dataclasses import dataclass

from HeatAndVentilationCoefficientCalculation.StaticData.SunRadiationHeat import SunRadiationHeat


@dataclass
class SunRadiationDataModel:
	name: str = "Москва"
	N: float = SunRadiationHeat["N"]
	S: float = SunRadiationHeat["S"]
	E: float = SunRadiationHeat["E"]
	W: float = SunRadiationHeat["W"]
	NW: float = SunRadiationHeat["NW"]
	NE: float = SunRadiationHeat["NE"]
	SE: float = SunRadiationHeat["SE"]
	SW: float = SunRadiationHeat["SW"]
