from HeatAndVentilationCoefficientCalculation.VentilationCalculation.VentilationCalculationUtility import air_local_mass
from Utils.RenderModel import RenderModel


class WindowInfiltration:

	def __init__(self, height_building, t_out, t_in, air_velocity):
		"""
		требуемое сопротивление воздухопроницанию окон и балконных дверей и входных наружных дверей,
		  t_in- расчетная температура внутреннего воздуха здания
		  t_out - средняя температура наружного воздуха
		  height_building - высота здания (от уровня пола первого этажа до верха вытяжной шахты), м;
		"""
		self.height_building = height_building
		self.t_out = t_out
		self.t_in = t_in
		self.air_velocity = air_velocity

	def delta_pressure_window(self) -> RenderModel:
		"""
	    требуемое сопротивление воздухопроницанию окон
	    """
		r_out = round(air_local_mass(self.t_out))
		r_in = round(air_local_mass(self.t_in))
		delta_pressure = 0.55 * self.height_building * (r_out - r_in) + (0.03 * r_out * self.air_velocity ** 2)
		output_value = round(delta_pressure, 1)
		output_render_value = f"""dPок=0.55 * {self.height_building} * ({r_out} - {r_in}) + 0.03 * {r_out} * {self.air_velocity} ** 2= {0.55 * self.height_building * (r_out - r_in)}+{(0.03 * r_out * self.air_velocity ** 2)}={output_value}"""
		multiply_render = RenderModel("Разность давлений воздуха на наружной и внутренней сторонах окон",
		                              output_value=output_value,
		                              output_render_value=output_render_value,
		                              key="delta_pressure_window")
		return multiply_render

	def delta_pressure_door(self) -> RenderModel:
		"""
	    требуемое сопротивление воздухопроницанию окон и балконных дверей и входных наружных дверей,
	      t_in- расчетная температура внутреннего воздуха здания
	      t_out - средняя температура наружного воздуха
	      height_building - высота здания (от уровня пола первого этажа до верха вытяжной шахты), м;
	    """
		r_out = air_local_mass(self.t_out)
		r_in = air_local_mass(self.t_in)
		delta_pressure = 0.28 * self.height_building * (r_out - r_in) + (0.03 * r_out * self.air_velocity ** 2)
		output_value = delta_pressure
		output_render_value = f"dPок=0.28 * {self.height_building} * ({r_out} - {r_in}) + 0.03 * {r_out} * {self.air_velocity} ** 2={delta_pressure}"
		multiply_render = RenderModel("Разность давлений воздуха на наружной и внутренней сторонах дверей",
		                              output_value=output_value,
		                              output_render_value=output_render_value,
		                              key="delta_pressure_door")
		return multiply_render

	def g_inf_window(self, windows_area: float) -> RenderModel:
		"""инфильтрация через окна"""
		output_value = windows_area / 0.9 * (self.delta_pressure_window().output_value / 10) ** (2 / 3)
		output_render_value = f"{windows_area} / 0.9 * ({self.delta_pressure_window().output_value}**(2/3) / 10)={output_value}"
		multiply_render = RenderModel("инфильтрация воздуха через окна",
		                              output_value=output_value,
		                              output_render_value=output_render_value,
		                              key="g_inf_window"
		                              )
		return multiply_render

	def g_inf_doors(self, doors_area: float) -> RenderModel:
		"""инфильтрация через двери"""
		output_value = doors_area / 0.9 * (self.delta_pressure_door().output_value / 10) ** (1 / 2)
		output_render_value = f"{doors_area} / 0.13 * ({self.delta_pressure_door().output_value}**(2/3) / 10)={output_value}"
		multiply_render = RenderModel("инфильтрация воздуха через двери",
		                              output_value=output_value,
		                              output_render_value=output_render_value,
		                              key="g_inf_doors")
		return multiply_render