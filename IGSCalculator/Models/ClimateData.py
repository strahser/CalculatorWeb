from dataclasses import dataclass, field


@dataclass()
class ClimateData:
	t_ot_middle: float  # Средняя температура наружного воздуха за отопительный период	textav , °С
	t_out_max: float  # Расчетная температура наружного воздуха	  text , °С		-26
	z_ot: float  # Продолжительность отопительного периода	zht , cут.
	air_velocity_middle: float
	air_velocity_max: float
	t_in: float = 20  # Расчетная температура внутреннего воздуха	  tint , °С
	GSOP: float = field(init=False)

	def __post_init__(self):
		self.GSOP = (self.t_in - self.t_ot_middle) * self.z_ot
