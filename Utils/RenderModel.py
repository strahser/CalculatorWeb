from dataclasses import dataclass, field


@dataclass()
class RenderModel:
	render_name: str
	output_value: float
	output_render_value: str
	key: str

	def get_render_dictionary(self) -> dict[str, str]:
		return {self.key: self.output_render_value}

	@staticmethod
	def create_string_list_sum(func_name: str, iterable_: list, arithmetic_operator: str = "+") -> str:
		"""
		возвращает строку в ввиде арифмитечских операций переданного метода переданного итератора
		"""
		join_list = [
			str(round(getattr(val, func_name)(), 1))
			if isinstance(getattr(val, func_name)(), float | int)
			else str(getattr(val, func_name)())
			for val in iterable_
		]
		return arithmetic_operator.join(join_list)


@dataclass()
class RenderModelList:
	render_name: str
	output_value: float
	output_render_list: list[RenderModel]
	key: str
