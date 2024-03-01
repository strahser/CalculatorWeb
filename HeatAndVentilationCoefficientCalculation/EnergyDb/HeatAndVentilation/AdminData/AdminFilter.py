from HeatAndVentilationCoefficientCalculation.StaticData.OrientationData import OrientationData
from django.db.models import Q
from django.contrib import admin
from HeatAndVentilation.models.BaseStructure import BaseStructure
from HeatAndVentilation.models.Building import Building
from HeatAndVentilation.models.Room import Room
from HeatAndVentilation.models.Structure import Structure
from HeatAndVentilation.models.StructureLayer import StructureLayer
from HeatAndVentilationCoefficientCalculation.StaticData.StructureTypeData import StructureTypeData


class BuildingFilter(admin.SimpleListFilter):
	title = "Здание"
	parameter_name = 'building_id'

	def lookups(self, request, model_admin):
		qs = Building.objects.all()
		return [(building.id, building.name) for building in qs]

	def queryset(self, request, queryset):
		"""
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via`self.value()`.
        """
		if self.value():
			qs_filter = queryset.filter(room__building__id=self.value())
			return qs_filter
		else:
			return queryset


class RoomFilter(admin.SimpleListFilter):
	title = "Помещение"
	parameter_name = 'room_id'

	def lookups(self, request, model_admin):
		look_up = 'building_id'
		request_data = request.GET.get(look_up)
		if request_data:
			qs_room = Room.objects.filter(building_id=request_data). \
				values_list('id', 'name').distinct()
			return qs_room
		else:
			qs_room = Room.objects.values_list('id', 'name').all()
			return qs_room

	def queryset(self, request, queryset):
		"""
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via`self.value()`.
        """

		if self.value():
			qs_filter = queryset.filter(room__id=self.value())
			return qs_filter
		else:
			return queryset


class StructureFilter(admin.SimpleListFilter):
	title = "Конструкции"
	parameter_name = 'structure_name'

	def lookups(self, request, model_admin):
		room_data = request.GET.get('room_id')
		building_data = request.GET.get('building_id')
		look_up_render = 'base_structures__standard_structure_type', 'base_structures__standard_structure_type'
		qs = Structure.objects.filter(Q(room_id=room_data) & Q(room__building_id=building_data))
		return_tuple = qs.values_list(*look_up_render).distinct()
		return_tuple_change = [(key, getattr(StructureTypeData, val).value) for key, val in return_tuple]
		if return_tuple:
			return return_tuple_change
		else:
			qs_all = Structure.objects.values_list(*look_up_render).distinct()
			return_tuple_change_all = [(key, getattr(StructureTypeData, val).value) for key, val in qs_all if
			                           hasattr(StructureTypeData, val)]
			return return_tuple_change_all

	def queryset(self, request, queryset):
		"""
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via`self.value()`.
        """
		if self.value():
			qs_filter = queryset.filter(base_structures__standard_structure_type=self.value())
			return qs_filter
		else:
			return queryset


class OrientationFilter(admin.SimpleListFilter):
	title = "Ориентация"
	parameter_name = 'orientation_name'

	def lookups(self, request, model_admin):
		room_data = request.GET.get('room_id')
		building_data = request.GET.get('building_id')
		structure_name = request.GET.get('structure_name')
		look_up_render = 'orientation', 'orientation'
		qs = Structure.objects.filter(
			Q(room_id=room_data) &
			Q(room__building_id=building_data) &
			Q(base_structures__standard_structure_type=structure_name)
		)
		return_tuple = qs.values_list(*look_up_render).distinct()
		return_tuple_change = [(key, getattr(OrientationData, val).value) for key, val in return_tuple]
		if return_tuple:
			return return_tuple_change
		else:
			qs_all = Structure.objects.values_list(*look_up_render).distinct()
			return_tuple_change_all = [(key, getattr(OrientationData, val).value) for key, val in qs_all]
			return return_tuple_change_all

	def queryset(self, request, queryset):
		"""
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via`self.value()`.
        """
		if self.value():
			qs_filter = queryset.filter(base_structures__standard_structure_type=self.value())
			return qs_filter
		else:
			return queryset


class StructureDetailFilter(admin.SimpleListFilter):
	title = 'Детали констр.'
	parameter_name = 'short_name'

	def lookups(self, request, model_admin):
		all_structures_qs = Structure.objects.all()

		building_id = request.GET.get('building_id')
		room_id = request.GET.get('room_id')
		orientation__exact = request.GET.get('orientation_name')
		structure_id = request.GET.get('structure_name')

		qs = Structure.objects.filter(
			Q(base_structures__standard_structure_type=structure_id) |
			Q(room__building_id=building_id) |
			Q(room__id=room_id) |
			Q(orientation=orientation__exact)
		).distinct()
		if qs:
			return qs.values_list("short_name", "short_name")
		else:
			return all_structures_qs.distinct(). \
				values_list("short_name", "short_name")

	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(short_name=self.value())
		else:
			return queryset
