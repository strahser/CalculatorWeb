from django.db import models

from StaticDB.models.StandardStructureLayer import StandardStructureLayer


class StructureLayer(models.Model):
    """Базовый шаблон от справочных данных по конструкциям. добавляем толщину материала и фотографию.
        т.к. лямбда дублируется со значением поля справочных данных, выносим ее в расчитываемый коэффициент.
        пользоватлеь на прямую не видит эту таблицы. взаимодействие происходит в рамках выбора при конструировании базового слоя

    """
    name = models.CharField(max_length=100, verbose_name="наименование материала")
    thickness_layer = models.FloatField(verbose_name="Толщина материала,мм", default=1)
    standard_structure_layer = models.ForeignKey(StandardStructureLayer,
                                                 verbose_name="наименование базового слоя материала",
                                                 on_delete=models.DO_NOTHING, )
    base_structure = models.ForeignKey("HeatAndVentilation.BaseStructure",
                                       verbose_name="базовая конструкция",
                                       on_delete=models.CASCADE)
    structure_picture_layer = models.ImageField(verbose_name="Изображение",
                                                blank=True,
                                                upload_to="Structurlayer/%Y/%m/%d/")
    creation_stamp = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    update_stamp = models.DateTimeField(auto_now=True, verbose_name="дата изменения")

    @property
    def R_structure_layer(self):
        return round(self.thickness_layer * 0.001 / self.lambda_structure_layer, 2)

    @property
    def lambda_structure_layer(self):
        return self.standard_structure_layer.lambda_structure_layer

    lambda_structure_layer.fget.short_description = "коэфф. теплопроводности λ(Б) Вт/(м•°С)"

    def __str__(self):
        return f"Наим: {self.name} Тол:{self.thickness_layer} Теплопр.:{self.lambda_structure_layer}"

    class Meta:
        verbose_name = "Слой Конструкции"
        verbose_name_plural = "Слои Конструкций"
