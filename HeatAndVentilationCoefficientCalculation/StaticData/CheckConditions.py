from linque import linque

from HeatAndVentilationCoefficientCalculation.StaticData.StaticCoefficientStructures import StaticCoefficientStructures
from Utils.RenderModel import RenderModel


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
	def k_total_norm(gsop: float, building_volume: float)->RenderModel:
		"""Нормируемое значение удельной теплозащитной характеристики здания определяется по формуле (5.5)
        1 Для промежуточных значений величин объема зданий и ГСОП, а также для зданий с отапливаемым объемом более
        200 000   значение   рассчитываются по формулам k_total_ge_960,k_total_le_960,k_total_max
        2 При достижении величиной  , вычисленной по (k_total_ge_960,k_total_le_960), значений меньших,
        чем определенных по формуле (k_total_max), следует принимать значения   определённые по формуле (k_total_max).
        """

		def k_total_ge_960():
			b_v = building_volume ** (1 / 2)
			up = 0.16 + (10 / b_v)
			down =0.00013 * gsop + 0.61
			output_value = up / down
			output_render_value = f"0.16 + (10 / {building_volume} ** (1 / 2)) / 0.00013 * {gsop} + 0.61 = {round(output_value,2)}"
			return RenderModel(render_name="Нормируемое значение удельной теплозащитной характеристики здания",
			            output_value=output_value,
			            output_render_value=output_render_value,
			            key="k_total_ge_960")

		def k_total_le_960():
			up = 4.74 / (0.00013 * gsop + 0.61)
			b_v = building_volume ** (1 / 3)
			down = 1/b_v
			output_value =up * down
			output_render_value = f"4.74 / (0.00013 * {gsop} + 0.61) *1/ {building_volume} ^(1 / 3) ={round(output_value,2)}"
			return RenderModel(render_name="Нормируемое значение удельной теплозащитной характеристики здания",
			            output_value=output_value,
			            output_render_value=output_render_value,
			            key="k_total_le_960")

		def k_total_max(gsop):
			output_value =8.5 / (gsop ** 1 / 2)
			output_render_value = f"8.5 / ({gsop} ^ 1 / 2) ={round(output_value,2)}"
			return RenderModel(render_name="Нормируемое значение удельной теплозащитной характеристики здания",
			            output_value=output_value,
			            output_render_value=output_render_value,
			            key="k_total_max")


		k_total_value = k_total_ge_960() if building_volume > 960 else k_total_le_960()
		k_total_max_value = k_total_max(gsop)
		maximum_value = k_total_max_value if k_total_max_value.output_value> k_total_value.output_value else k_total_value
		output_value = maximum_value.output_value
		output_render_value = maximum_value.output_render_value
		return RenderModel(render_name="Нормируемое значение удельной теплозащитной характеристики здания",
		            output_value=output_value,
		            output_render_value=output_render_value,
		            key="k_total_norm")

