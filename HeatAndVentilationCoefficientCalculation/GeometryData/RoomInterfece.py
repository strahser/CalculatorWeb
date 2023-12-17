from abc import ABC, abstractmethod


class RoomI(ABC):
	"""поля класса необходимы для расчета вентиляции"""
	@property
	@abstractmethod
	def window_area(self):
		raise NotImplementedError

	@property
	@abstractmethod
	def door_area(self):
		raise NotImplementedError

	@property
	@abstractmethod
	def floor_area_heated(self):
		raise NotImplementedError

	@property
	@abstractmethod
	def floor_area_living(self):
		raise NotImplementedError

	@property
	@abstractmethod
	def human_number(self):
		raise NotImplementedError
