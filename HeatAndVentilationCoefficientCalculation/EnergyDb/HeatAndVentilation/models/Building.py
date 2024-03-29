import json
import os.path
from django.db import models
import HeatAndVentilationCoefficientCalculation.StaticData.RenamedRenderDfColumns
from StaticDB.models.ClimateData import ClimateData
from HeatAndVentilationCoefficientCalculation.StaticData.BuildingCategory import BuildingCategory
from HeatAndVentilationCoefficientCalculation.RenderData.RenderData import render_data
import pandas as pd
from dacite import from_dict
from HeatAndVentilationCoefficientCalculation.SpaceData.BuildingDataModel import BuildingDataModel
from HeatAndVentilationCoefficientCalculation.EnergyDb.Utils.TableRender import df_html
from HeatAndVentilationCoefficientCalculation.EnergyDb.Utils.URLS import get_root_dir
from HeatAndVentilationCoefficientCalculation.StaticData.RenamedRenderDfColumns import renamed_columns,tabs_titles


class Building(models.Model):
	name = models.CharField(max_length=150, verbose_name="наименование", default="Здание1")
	category = models.CharField(max_length=150, choices=[(val.name, val.value) for val in BuildingCategory],
	                            default=BuildingCategory.living.name,
	                            verbose_name="категория помещения")
	climate_data = models.ForeignKey(ClimateData, on_delete=models.DO_NOTHING, verbose_name="климат.данные")
	building_temperature = models.FloatField(verbose_name="внутренняя температура °С", default=20)
	heated_volume = models.FloatField(verbose_name="отапливаемый объем м3", default=34229)
	level_number = models.IntegerField(verbose_name="количество этажей", default=20)
	level_height = models.FloatField(verbose_name="высота этажа,м", default=3)
	creation_stamp = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
	update_stamp = models.DateTimeField(auto_now=True, verbose_name="дата изменения")

	class Meta:
		verbose_name = "01 Здание"
		verbose_name_plural = "01 Здания"

	@property
	def GSOP(self):
		return (self.building_temperature - self.climate_data.t_ot_middle) * self.climate_data.z_ot

	GSOP.fget.short_description = 'ГСОП'

	@staticmethod
	def make_heat_calculations(response_data_: dict) -> dict:
		"""создаем данные для вкладок, в ввиде df. Фильтруем и переименовываем данные response_data_
        excluding_list -уже созданные data frame из response_data_
        """

		def get_renamed_data_dict():
			root_dir = get_root_dir()
			renamed_dict_path = os.path.join(root_dir, 'StaticData', 'renamed_text.json')
			with open(renamed_dict_path, encoding='utf-8') as f:
				return json.load(f)

		excluding_list = ["df", "df_group", "df_window_group"]
		new_data_dict = {}
		data_list = from_dict(data_class=BuildingDataModel, data=response_data_)
		res = render_data(data_list)
		data_dict = {key: val for key, val in res.items() if key not in excluding_list}
		df_data = {"Наименование расчетных параметров": data_dict.keys(), "Расчетное значение": data_dict.values()}
		df_data_df = pd.DataFrame(df_data)
		renamed_data = get_renamed_data_dict()
		df_data_df = df_data_df.replace(renamed_data)
		df_data_df = df_data_df.to_html(index=False, classes="table table-striped table-bordered ", border=1)
		new_data_dict['energy_passport'] = "<h4 class='heading'> Удельная теплозащитная характеристика здания </h4>" + df_data_df
		for en, val in enumerate(excluding_list):
			new_data_dict[val] = f"<h4 class='heading'>{tabs_titles[en]}</h4>" + df_html(res[val].rename(
				columns=renamed_columns
			)
			)
		return new_data_dict

	def __str__(self):
		return f"{self.name} город {self.climate_data.name}"
