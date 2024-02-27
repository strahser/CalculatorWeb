from dataclasses import dataclass, field

from HeatAndVentilationCoefficientCalculation.ProjectData.SunRadiationDataModel import SunRadiationDataModel


@dataclass()
class ClimateDataModel:
	name: str = 'Москва'
	t_out_max: float = -26  # Расчетная температура наружного воздуха	  text , °С		-26
	z_ot: float = 204  # Продолжительность отопительного периода	zht , cут.
	t_ot_middle: float = -2, 2  # Средняя температура наружного воздуха за отопительный период	textav , °С
	air_velocity_middle: float = 3, 8
	air_velocity_max: float = 3, 8
	t_in: float = 20  # Расчетная температура внутреннего воздуха	  tint , °С
	sun_radiation: SunRadiationDataModel = field(default_factory=SunRadiationDataModel)

	def __post_init__(self):
		self.GSOP = (self.t_in - self.t_ot_middle) * self.z_ot
