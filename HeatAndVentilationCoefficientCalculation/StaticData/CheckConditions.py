from HeatAndVentilationCoefficientCalculation.StaticData.StaticCoefficientStructures import StaticCoefficientStructures


class CheckConditions:
	@staticmethod
	def check_k_comp_value(k_comp: float, level_number: int) -> str:
		"""проверяем коэффициент компактности здания"""

		#
		if 1 <= level_number <= 3:
			res = ""
			for k, v in StaticCoefficientStructures.check_compact_level_coefficient.items():
				if k_comp < StaticCoefficientStructures.check_compact_level_coefficient[level_number]:
					res = f"Проверка компактности здания пройдена {round(k_comp, 1)} <= {StaticCoefficientStructures.check_compact_level_coefficient[level_number]}"
				else:
					res = f"Проверка компактности здания не пройдена {round(k_comp, 1)} >= {StaticCoefficientStructures.check_compact_level_coefficient[level_number]}"
			return res
		else:
			return f"количество этажей {level_number} вне диапазона расчета"

	@staticmethod
	def k_total_norm(gsop: float, building_volume: float):
		"""Нормируемое значение удельной теплозащитной характеристики здания определяется по формуле (5.5)
        1 Для промежуточных значений величин объема зданий и ГСОП, а также для зданий с отапливаемым объемом более
        200 000   значение   рассчитываются по формулам k_total_ge_960,k_total_le_960,k_total_max
        2 При достижении величиной  , вычисленной по (k_total_ge_960,k_total_le_960), значений меньших,
        чем определенных по формуле (k_total_max), следует принимать значения   определённые по формуле (k_total_max).
        """

		def k_total_ge_960():
			up = 4.74 / (0.00013 * gsop + 0.61)
			down = building_volume ** (1 / 3)
			return up / down

		def k_total_le_960():
			b_v = building_volume ** (1 / 2)
			up = 0.16 + (10 / b_v)
			down = 0.00013 * gsop + 0.61
			return up / down

		def k_total_max(gsop):
			return 8.5 / (gsop ** 1 / 2)

		# print(f"k_total_ge_960={k_total_ge_960} k_total_le_960={k_total_le_960} k_total_max={k_total_max}")
		k_total = k_total_ge_960() if building_volume > 960 else k_total_le_960()
		k_total_max = k_total_max(gsop)
		return k_total if k_total > k_total_max else k_total_max