from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from HeatAndVentilation.AdminData.AdminFilter import BuildingFilter, RoomFilter, StructureFilter, StructureDetailFilter
from HeatAndVentilation.forms import StructureForm
from HeatAndVentilation.models.BaseStructure import BaseStructure
from HeatAndVentilation.models.Structure import Structure
from HeatAndVentilation.models.StructureLayer import StructureLayer
from HeatAndVentilationCoefficientCalculation.EnergyDb.Utils.AdminUtils import duplicate_event, \
    get_standard_display_list
from HeatAndVentilationCoefficientCalculation.StaticData.StructureTypeData import StructureTypeData
from django.utils.safestring import mark_safe


class CustomAdminSite(AdminSite):
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            "Building": 1,
            "Room": 2,
            "BaseStructure": 3,
        }
        app_dict = self._build_app_dict(request)
        # a.sort(key=lambda x: b.index(x[0]))
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list


@admin.register(Structure)
class ConstructionDataAdmin(admin.ModelAdmin):
    list_display = get_standard_display_list(
        Structure,
        excluding_list=['n_temperature_coefficient'],
        additional_list=['standard_structure_type_display', 'R_real',
                         'R_Norm_conditional_display']
    )
    list_display_links = ('id', 'name')
    list_filter = [BuildingFilter, RoomFilter, StructureFilter, StructureDetailFilter]
    list_per_page = 10
    actions = [duplicate_event]
    form = StructureForm

    @admin.display(description="Стандартные конструкции")
    def standard_structure_type_display(self, instance: Structure):
        return getattr(StructureTypeData, instance.standard_structure_type).value

    @admin.display(description='R Normative')
    def R_Norm_conditional_display(self, instance: Structure):
        if instance.R_Norm > instance.R_real:
            return format_html(
                f'<div style="width:100%%; height:100%%; background-color:orange;">{round(instance.R_Norm, 2)}</div>')
        else:
            return round(instance.R_Norm, 2)


@admin.register(BaseStructure)
class ConstructionDataAdmin(admin.ModelAdmin):
    list_display = get_standard_display_list(BaseStructure)
    list_display_links = ('id', 'name')
    list_per_page = 10
    actions = [duplicate_event]


@admin.register(StructureLayer)
class StructureLayerDataAdmin(admin.ModelAdmin):
    list_display = get_standard_display_list(StructureLayer, ['structure_picture_layer', 'post_photo'])
    list_display_links = ('id', 'name')
    readonly_fields = ['post_photo']
    list_per_page = 10
    actions = [duplicate_event]

    @admin.display(description="Изображение")
    def post_photo(self, structure_type: StructureLayer):
        if structure_type.structure_picture_layer:
            return mark_safe(f"<img src='{structure_type.structure_picture_layer.url}' width=50>")
        else:
            return "Без изображения"
