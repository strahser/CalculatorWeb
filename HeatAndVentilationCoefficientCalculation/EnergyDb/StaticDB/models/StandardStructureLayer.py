from django.db import models


class StandardStructureLayer(models.Model):
	name = models.TextField(verbose_name="наименование материала",default='Минеральная (каменная) вата 170-220 кг/м³')
	c = models.FloatField(verbose_name="Удельная теплоемкость кДж/(кг•°С)", default=0.84)
	lambda_structure_layer = models.FloatField(verbose_name="коэфф. теплопроводности λ(Б) Вт/(м•°С)", default=0.043)
	m = models.FloatField(verbose_name="Коэффициент паропроницаемости  мг/(м•ч•Па)", default=0.55)
	creation_stamp = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
	update_stamp = models.DateTimeField(auto_now=True, verbose_name="дата изменения")

	def __str__(self):
		return f"Наим: {self.name}  Теплопр.:{self.lambda_structure_layer}"

	class Meta:
		verbose_name = "Базовый Слой Конструкции"
		verbose_name_plural = "Базовый Слои Конструкций"