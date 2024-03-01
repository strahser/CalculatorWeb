from django.contrib import admin
from HeatAndVentilation.models.BaseStructure import BaseStructure
from HeatAndVentilation.models.Building import Building
from HeatAndVentilation.models.Room import Room
from HeatAndVentilation.models.Structure import Structure
from HeatAndVentilation.models.StructureLayer import StructureLayer
from django.urls import reverse
from django.utils.safestring import mark_safe
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedInline


# region Inline (foregien key to object)
class EditLinkToInlineObject(object):
	def edit_link(self, instance):
		url = reverse('admin:%s_%s_change' % (
			instance._meta.app_label,
			instance._meta.model_name),
		              args=[instance.pk])
		if instance.pk:
			return mark_safe(f'<div style="width:100%%; height:100%%; color:red; font-size:16px; font-weight:bolder;"><a href="{url}">ссылка на конструкции</a></div>')
		else:
			return ''


class ClimateInline(admin.TabularInline):
	model = Building
	extra = 0
	can_delete = True
	show_change_link = True


class StructureInlineTabular(admin.TabularInline):
	model = Structure
	extra = 0


class StructureInline(NestedStackedInline):
	model = Structure
	extra = 0
	fk_name = 'room'


class RoomInline(EditLinkToInlineObject, admin.TabularInline):
	model = Room
	extra = 0
	can_delete = True
	show_change_link = True
	readonly_fields = ('edit_link',)
# fk_name = 'building'
# inlines = [StructureInline]


class StructureTypeInline(admin.TabularInline):
	model = BaseStructure
	extra = 0


class StructureLayerInline(admin.TabularInline):
	model = StructureLayer
	extra = 0
	can_delete = True
	show_change_link = True

	def lambda_structure_layer(self, obj):
		return obj.order.lambda_structure_layer


class BaseStructureInline(admin.TabularInline):
	model = BaseStructure
	extra = 0

# endregion
