from pprint import pprint

from django.db import models
import pandas as pd
from django.urls import reverse
from django.utils.safestring import mark_safe
from typing import Iterable

from django_pandas.io import read_frame

from HeatAndVentilation.models.Structure import Structure
from HeatAndVentilation.models.StructureLayer import StructureLayer
from HeatAndVentilationCoefficientCalculation.HeatCalculation.StructureThermalResistenceCoefficient import \
	get_normative_thermal_resistence_coefficient
from HeatAndVentilationCoefficientCalculation.StaticData.StructureTypeData import StructureTypeData
from HeatAndVentilationCoefficientCalculation.EnergyDb.Utils.TableRender import render_modal_window, button_link, \
	create_table_from_model, create_reverse_button, create_group_button, create_crud_buttons, ButtonData
from HeatAndVentilationCoefficientCalculation.EnergyDb.Utils.TableRender import df_html
from HeatAndVentilationCoefficientCalculation.EnergyDb.Utils.AdminUtils import get_standard_display_list
from typing import List


class BaseStructure(models.Model):
	"""шаблон типовых конструкций, без конкретной площади. Например навесной фасад.
    Состоит из множества слоев. Опционально можем расчитать ГСОП конструкции и получить нормируемый коэффицент теплопередачи,
    если выберим здания/здание (множественный выбор)

    """
	name = models.TextField(max_length=90, verbose_name="наименование")
	R_custom = models.FloatField(verbose_name="Введенное.терм. сопр.", null=False, blank=False, default=1,
	                             help_text="принимается в расчетах если не заданы слои конструкций")
	standard_structure_type = models.CharField(max_length=60,
	                                           choices=[(val.name, val.value) for val in StructureTypeData],
	                                           blank=False,
	                                           default=StructureTypeData.Wall,
	                                           verbose_name="тип",
	                                           )
	buildings_list = models.ManyToManyField(
		"HeatAndVentilation.Building", verbose_name="связанные здания",
		blank=True,
		help_text="Опционально, если необходимо сравнить нормируемые термические сопротивления для разных зданий, "
		          "с рассчитанным")
	structure_picture = models.ImageField(verbose_name="Изображение", blank=True, upload_to="StructureType/%Y/%m/%d/")
	creation_stamp = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
	update_stamp = models.DateTimeField(auto_now=True, verbose_name="дата изменения")

	def __str__(self):
		return f"{self.name}  {self.standard_structure_type}"

	class Meta:
		verbose_name = "Базовая конструкция"
		verbose_name_plural = "Базовые конструкции"
		ordering = ['id']

	@property
	def R_calculated(self):
		layers_qs = StructureLayer.objects.filter(base_structure__id=self.id)
		if layers_qs:
			r_calc = [val.thickness_layer * 0.001 / val.lambda_structure_layer for val in layers_qs]
			R_tr_val = round(1 / 23 + sum(r_calc) + 1 / 8.7, 2)
			return R_tr_val

	@property
	def R_real(self):
		return self.R_calculated if self.R_calculated else self.R_custom

	@property
	def R_norm(self):
		qs1 = BaseStructure.objects.filter(pk=self.pk).prefetch_related(
			'buildings_list').first().buildings_list.all()
		data = self.render_gsop_table(qs1, self.standard_structure_type)[0]
		df = pd.DataFrame(data)
		if not df.empty:
			return mark_safe(df_html(df[["Город", 'R_норматив']]))

	@property
	def calculate_heat_resistance_normative(self):
		try:
			qs1 = BaseStructure.objects.filter(pk=self.pk). \
				prefetch_related('buildings_list').first().buildings_list.all()
			modal_body = self.render_gsop_table(qs1, self.standard_structure_type)[1]
			all_index = [v["id"] for v in Structure.objects.all().values("id")]
			max_pk = max(all_index) if all_index else 0
			res = render_modal_window(pk=self.pk + max_pk + 100, title=self.name, modal_body=modal_body)
			return mark_safe(res)
		except:
			return ""

	calculate_heat_resistance_normative.fget.short_description = 'Терм. сопрот.расчетное'

	@staticmethod
	def render_gsop_table(building_qs: Iterable, standard_structure_type: str, layers_qs: Iterable = None):
		gsop_list = [val.get_gsop for val in building_qs]
		R_norm = [get_normative_thermal_resistence_coefficient(gsop).get(standard_structure_type) for gsop in gsop_list]
		data = {"Здание": [val.name for val in building_qs],
		        "Город": [val.climate_data.name for val in building_qs],
		        "ГСОП": gsop_list,
		        "R_норматив": R_norm
		        }
		df = pd.DataFrame(data)
		if not df.empty:
			return data, df_html(pd.DataFrame(df))

	@staticmethod
	def display_layers_create_table(layers_qs: models.query) -> str:
		if layers_qs:
			df = create_table_from_model(StructureLayer, layers_qs,filter_columns=['name', 'thickness_layer'])
			group_buttons_data = [
				ButtonData('HeatAndVentilation:StructureLayerCopyView', 'pk', 'success', 'скопировать'),
				ButtonData('HeatAndVentilation:StructureLayerUpdateView', 'pk', 'info', 'обновить'),
				ButtonData('HeatAndVentilation:StructureLayerDeleteView', 'pk', 'danger', 'удалить'),
			]
			df.index.name = "номер слоя"
			df.index = df.index + 1
			df["&lambda;"] = [val.lambda_structure_layer for val in layers_qs]
			df["&delta;/&lambda;"] = [val.R_structure_layer for val in layers_qs]
			df['url'] = create_crud_buttons(layers_qs, group_buttons_data)
			df.loc["Итого"] = df.sum(numeric_only=True)
			df = df.fillna("")
			return mark_safe(df_html(df, index=True))
		else:
			return ""

	@property
	def display_layers(self):
		qs = StructureLayer.objects.filter(base_structure=self.pk)
		title = f"Конструкция базовго слоя {BaseStructure.objects.filter(pk=self.pk).first().name}"
		data = self.display_layers_create_table(qs)
		url_list = reverse('HeatAndVentilation:StructureLayerCreateView', kwargs={'base_pk': self.pk})
		button = button_link(url_list, cls='info', name='создать')
		if data:
			modal_body = f"{data}"
			return mark_safe(render_modal_window(pk=self.pk, title=title, modal_body=modal_body) + button)
		else:
			return mark_safe("--------------" + button)

	display_layers.fget.short_description = 'Слои Конструкции'
