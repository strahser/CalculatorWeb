from django.db import models
from django.urls import reverse

from HeatAndVentilationCoefficientCalculation.HeatCalculation.StructureThermalResistenceCoefficient import \
    get_normative_thermal_resistence_coefficient

from HeatAndVentilationCoefficientCalculation.StaticData.OrientationData import OrientationData
from django.utils.html import format_html

from HeatAndVentilationCoefficientCalculation.StaticData.StructureTypeData import StructureTypeData


class Structure(models.Model):
    name = models.CharField(max_length=90, verbose_name="наименование")
    area = models.FloatField(verbose_name="площадь ", null=False)
    base_structures = models.ForeignKey("HeatAndVentilation.BaseStructure",
                                        verbose_name="Базовая конструкция",
                                        on_delete=models.CASCADE,
                                        related_name='base_structure')

    orientation = models.CharField(
        max_length=3, blank=False, null=False, choices=[(val.name, val.value) for val in OrientationData],
        verbose_name="ориентация", default=OrientationData.ND.name
    )
    room = models.ForeignKey("HeatAndVentilation.Room", verbose_name="Помещение", on_delete=models.CASCADE,
                             related_name='rooms', null=True)

    short_name = models.CharField(max_length=15, blank=True, verbose_name="краткое наименование")
    creation_stamp = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    update_stamp = models.DateTimeField(auto_now=True, verbose_name="дата изменения")

    class Meta:
        verbose_name = "Ограждающая конструкция"
        verbose_name_plural = "Ограждающие конструкции"
        ordering = ['base_structures__name']

    def __str__(self):
        return f"--{self.name}--{self.short_name}--"

    @property
    def R_real(self):
        qs = Structure.objects.get(pk=self.pk).base_structures.R_custom
        return qs

    @property
    def standard_structure_type(self):
        qs = Structure.objects.get(pk=self.pk).base_structures.standard_structure_type
        return qs

    @property
    def R_Norm(self):
        gsop = Structure.objects.get(pk=self.pk).room.building.get_gsop
        r_norm = get_normative_thermal_resistence_coefficient(gsop)[self.standard_structure_type]
        return round(r_norm, 2)

    @property
    def get_structures_update_view(self):
        my_url = reverse("StructureUpdateView", kwargs={"structure_pk": self.pk})
        return str(f"<a href='{my_url}'>{self.pk}</a>")
