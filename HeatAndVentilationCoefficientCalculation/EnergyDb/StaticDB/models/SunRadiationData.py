from django.db import models

from HeatAndVentilationCoefficientCalculation.StaticData.SunRadiationHeat import SunRadiationHeat


class SunRadiationData(models.Model):
	name = models.TextField(verbose_name="Наименование",default="Москва")
	N = models.FloatField(verbose_name="С", default=SunRadiationHeat["N"])
	S = models.FloatField(verbose_name="Ю", default=SunRadiationHeat["S"])
	E = models.FloatField(verbose_name="В", default=SunRadiationHeat["E"])
	W = models.FloatField(verbose_name="З", default=SunRadiationHeat["W"])
	NW = models.FloatField(verbose_name="СЗ", default=SunRadiationHeat["NW"])
	NE = models.FloatField(verbose_name="СВ", default=SunRadiationHeat["NE"])
	SE = models.FloatField(verbose_name="ЮВ", default=SunRadiationHeat["SE"])
	SW = models.FloatField(verbose_name="ЮЗ", default=SunRadiationHeat["SW"])
	creation_stamp = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
	update_stamp = models.DateTimeField(auto_now=True, verbose_name="дата изменения")

	def __str__(self):
		return f"город {self.name}"

	class Meta:
		verbose_name = "Солнечная радиация"
		verbose_name_plural = "Солнечная радиация"
