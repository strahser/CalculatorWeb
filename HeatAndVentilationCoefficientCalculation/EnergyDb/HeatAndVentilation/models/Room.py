from pprint import pprint

from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import pandas as pd
from pandas.io.formats.style import Styler

from HeatAndVentilation.models.Structure import Structure
from HeatAndVentilationCoefficientCalculation.EnergyDb.Utils.TableRender import render_modal_window, button_link, \
    create_crud_buttons, create_table_from_model, df_html, ButtonData, style_email_tables, create_table_style
from HeatAndVentilationCoefficientCalculation.StaticData.RoomCategory import RoomCategory


class Room(models.Model):
    """One to many Building"""
    name = models.CharField(max_length=60, verbose_name="наименование помещения", default="Жилое помещение")
    category = models.TextField(choices=[(val.name, val.value) for val in RoomCategory],
                                default=RoomCategory.living, verbose_name="категория помещения", max_length=30)
    human_number = models.BigIntegerField(default=332, verbose_name="количество людей", null=False)
    t_in_room = models.FloatField(default=20.0, verbose_name="внут. темп. ", null=False)
    room_heated_volume = models.FloatField(default=24751, verbose_name="объем", null=False)
    floor_area_living = models.FloatField(default=3793, verbose_name="жилая площадь", help_text="жилая площадь это")
    floor_area_heated = models.FloatField(default=13080, verbose_name="отапливаемая площадь",
                                          help_text="отапливаемая площадь это", null=False)
    building = models.ForeignKey(
        "HeatAndVentilation.Building",
        verbose_name="Здание",
        on_delete=models.CASCADE,
        related_name="buildings"
    )
    creation_stamp = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    update_stamp = models.DateTimeField(auto_now=True, verbose_name="дата изменения")

    class Meta:
        verbose_name = "02 Помещение"
        verbose_name_plural = "02 Помещения"

    def __str__(self):
        return self.name

    @property
    def structures_list(self):
        """create data of structure"""
        return Structure.objects.distinct().filter(room=self.pk)

    @property
    def get_room_structures_list(self):
        my_url = reverse("StructureListView", kwargs={"pk": self.pk})
        return format_html(f"<a href='{my_url}'>Детали</a>")

    get_room_structures_list.fget.short_description = 'Огражд. Конструкции'

    @property
    def display_room_structures(self):
        def format_func(row):
            highlight = 'background-color: lightcoral;'
            default = ''

            # must return one string per cell in this row
            if row['R факт.'] < row['R нормат.']:
                return [highlight, default]
            else:
                return [default, default]

        qs = self.structures_list
        group_buttons_data = [
            ButtonData('HeatAndVentilation:StructureCopyView', 'pk', 'success', 'скопировать'),
            ButtonData('HeatAndVentilation:StructureUpdateView', 'pk', 'info', 'обновить'),
            ButtonData('HeatAndVentilation:StructureDeleteView', 'pk', 'danger', 'удалить'),
        ]
        try:
            df = create_table_from_model(Structure, qs, filter_columns=['name', 'short_name', 'area'])
            df['R факт.'] = [val.R_real for val in qs]
            df['R нормат.'] = [val.R_Norm for val in qs]
            df['url'] = create_crud_buttons(qs, group_buttons_data)
            df.index = df.index + 1

            df_p = df.style. \
                apply(format_func, subset=['R факт.', 'R нормат.'], axis=1). \
                apply(style_email_tables, axis=1). \
                set_table_styles([*create_table_style()]). \
                format(precision=2). \
                _repr_html_()
            res = render_modal_window(pk=self.pk,
                                      title=self.name,
                                      modal_body=df_p)
            return mark_safe(res)

        except Exception as e:
            print("Конструкции помещения ошибка", e)
            return " "

    display_room_structures.fget.short_description = 'Конструкции помещения'
