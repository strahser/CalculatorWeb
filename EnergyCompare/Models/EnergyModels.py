
from dataclasses import dataclass, Field, field, asdict, fields
from enum import Enum
ClASS_DATA = {"A++": 0.4, "A+": 0.5, "A": 0.6, "B": 0.7, "C": 0.85, "D": 1, "E": 1.15, "F": 1.25, "G": 1.5}

class Constant(Enum):
	kwt_to_m_3 = 0.0973#Квт электричества в 1 м3 газа
	gas_coast = 8#стоимость 1 м3 газа
	co2_const = 1.85#выделение С02 на 1 м3 газа
	co2_coast = 20*80#стоимость С02 при курсе евро 80 руб

class BaseNames(Enum):
	base_name = "Базовые показатели"
	base_value = "удельный годовой расход энергоресурсов кВт·ч/м2"
	total_energy = "годовой расход энергоресурсов кВт·ч"
	energy_class = "Класс Энергоэффективности"
	gsop = "ГСОП"


@dataclass()
class InterpolateDb:
	gsop: int
	level: int
	q_base_norm: int
