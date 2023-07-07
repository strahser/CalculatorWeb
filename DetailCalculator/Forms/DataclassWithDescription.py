from dataclasses import dataclass, Field, field, asdict, fields


@dataclass
class DataclassWithDescription:
	"""all data for calculation"""
	Nж: int
	Nчел: int
	GSOP: float
	A_кв: float
	A_нж: float
	v_гв_ж: float
	v_гв_нж: float
	q_р_от: float
	V_от: float
	N_этаж: int
	alpha: float
	z_heat: float
	K_ef_h_w: float
	q_ee: float

