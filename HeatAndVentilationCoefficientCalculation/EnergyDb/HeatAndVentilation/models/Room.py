from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import pandas as pd
from HeatAndVentilation.models.Structure import Structure
from HeatAndVentilationCoefficientCalculation.EnergyDb.Utils.TableRender import render_modal_window, button_link
from HeatAndVentilationCoefficientCalculation.StaticData.RoomCategory import RoomCategory


class Room(models.Model):
    """One to many Building"""
    name = models.CharField(max_length=60, verbose_name="наименование помещения", default="Жилое помещение")
    category = models.TextField(choices=[(val.name, val.value) for val in RoomCategory],
                                default=RoomCategory.living, verbose_name="категория помещения")
    human_number = models.IntegerField(default=332, verbose_name="количество людей", null=False)
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
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"

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
        try:
            qs = self.structures_list
            url_list = [reverse('HeatAndVentilation:StructureUpdateView', kwargs={'pk': val.pk}) for val in qs]

            data = {"Наименование": [val.name for val in qs],
                    "сокр.наим": [val.short_name for val in qs],
                    "площадь": [val.area for val in qs],
                    "Конструкции": [button_link(my_url, cls='danger') for my_url in url_list],
                    }
            modal_body = pd.DataFrame(data).to_html(index=True, classes="table table-striped table-bordered ", border=1,
                                                    escape=False)
            res = render_modal_window(pk=self.pk, title=self.name, modal_body=modal_body)
            return mark_safe(res)

        except Exception as e:
            print("Конструкции помещения ошибка", e)
            return "--"

    display_room_structures.fget.short_description = 'Конструкции помещения'
