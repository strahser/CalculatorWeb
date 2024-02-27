from rest_framework_dataclasses.serializers import DataclassSerializer
from HeatAndVentilationCoefficientCalculation.GeometryData.StructuresDataModel import StructureDataModel
from HeatAndVentilationCoefficientCalculation.SpaceData.BuildingDataModel import BuildingDataModel
from HeatAndVentilationCoefficientCalculation.SpaceData.RoomDataModel import RoomDataModel
from rest_framework import serializers


class StructureModelSerializer(DataclassSerializer):
	# n_temperature_coefficient = serializers.ReadOnlyField()

	class Meta:
		dataclass = StructureDataModel
		fields = list(StructureDataModel.__annotations__.keys())


class RoomModelSerializer(DataclassSerializer):
	structures_list = StructureModelSerializer(source='rooms', many=True)

	class Meta:
		dataclass = RoomDataModel
		fields = list(RoomDataModel.__annotations__.keys())


class BuildingModelSerializer(DataclassSerializer):
	rooms = RoomModelSerializer(source='buildings', many=True)

	class Meta:
		dataclass = BuildingDataModel
		fields = list(BuildingDataModel.__annotations__.keys())
