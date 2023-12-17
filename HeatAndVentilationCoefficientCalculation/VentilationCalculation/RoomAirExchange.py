from Utils.RenderModel import RenderModel


class RoomVentilation:

	def __init__(self, floor_area_heated: float, floor_area_living: float, human_number: int, level_height: float):
		"""
        L_vent количество приточного воздуха в здание при неорганизованном
        притоке либо нормируемое значение	при механической вентиляции
        """
		self._floor_area_heated = floor_area_heated
		self._floor_area_living = floor_area_living
		self._human_number = human_number
		self._level_height = level_height
		self.multiplicity_air_render_model = []  # list for renders

	def _check_multiply_air_condition(self, area_to_human: float) -> RenderModel:
		"""определяем воздухообмен по кратностям (по площади пола) в зависимости от отношения
			площади на человека
		"""
		if area_to_human:
			if area_to_human <= 20:
				output_value = 3 * self._floor_area_living
				output_render_value = f"L1=3 * {self._floor_area_living}={3 * self._floor_area_living}"
				multiply_render = RenderModel("кратность по площади", output_value=output_value,
				                              output_render_value=output_render_value,key="check_multiply_air_condition")
				return multiply_render
			else:
				output_value = self._floor_area_living * self._level_height * 0.35
				output_render_value = f"{self._floor_area_living} * {self._level_height} * 0.358={self._floor_area_living * self._level_height * 0.358}"
				multiply_render = RenderModel("кратность по площади", output_value=output_value,
				                              output_render_value=output_render_value,key="check_multiply_air_condition")
				return multiply_render

	def _multiplicity_air(self):
		area_to_human = self._floor_area_heated / self._human_number
		area_to_human_str = f"{self._floor_area_heated} / {self._human_number}={area_to_human}"
		area_to_human_render = RenderModel(render_name="площадь на человека", output_value=area_to_human,
		                                   output_render_value=area_to_human_str,key="multiplicity_air")
		multiply_render = self._check_multiply_air_condition(area_to_human)
		self.multiplicity_air_render_model.append(area_to_human_render)
		self.multiplicity_air_render_model.append(multiply_render)
		return multiply_render

	def _human_air(self):
		"""Гигиенические нормы люди"""
		output_value = self._human_number * 30
		output_render_value = f"{self._human_number} * 30={output_value}"
		_render = RenderModel("гигенический воздухообмен", output_value=output_value,
		                      output_render_value=output_render_value,key="human_air")
		self.multiplicity_air_render_model.append(_render)
		return _render

	def max_air_change(self):
		"""максимальный воздухообмен"""
		multiplicity_air = self._multiplicity_air()
		human_air = self._human_air()
		if isinstance(multiplicity_air, RenderModel):
			output_value = max(multiplicity_air.output_value, human_air.output_value)
			output_render_value = f"Lmax = max(L1={multiplicity_air.output_value} L2= {human_air.output_value})={output_value}"
			_render = RenderModel("максимальный воздухообмен", output_value=output_value,
			                      output_render_value=output_render_value,key="max_air_change")
			self.multiplicity_air_render_model.append(_render)
			return _render