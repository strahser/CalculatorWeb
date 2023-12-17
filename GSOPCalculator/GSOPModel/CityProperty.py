from dataclasses import dataclass, field


@dataclass
class CityProperty:
	t_out: float
	t_ot_per: float
	z_ot_per: float
	t_in: float = 20
	gsop_value: float = field(init=False)
	gsop_str: str = field(init=False)

	def __post_init__(self):
		self.gsop_value = (self.t_in - self.t_ot_per) * self.z_ot_per
		self.gsop_str = f"({self.t_in} - {self.t_ot_per}) * {self.z_ot_per} = {self.gsop_value}"
