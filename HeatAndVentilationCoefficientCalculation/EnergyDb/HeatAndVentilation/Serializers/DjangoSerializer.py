from rest_framework import serializers

from HeatAndVentilation.models.BaseStructure import BaseStructure
from HeatAndVentilation.models.Building import Building
from HeatAndVentilation.models.Room import Room
from StaticDB.models.ClimateData import ClimateData


class BaseStructureDjangoSerializer(serializers.ModelSerializer):
	class Meta:
		model = BaseStructure
		fields = '__all__'


class RoomDjangoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = '__all__'

	def get_queryset(self):
		building = Building.objects.get(pk=self.kwargs.get('pk', None))
		rooms = Room.objects.filter(building=building)
		return rooms


class ClimateDataDjangoSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClimateData
		fields = '__all__'


class BuildingDjangoSerializer(serializers.ModelSerializer):
	climate_data = serializers.PrimaryKeyRelatedField(read_only=True)

	class Meta:
		model = Building
		fields = '__all__'
