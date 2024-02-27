from HeatAndVentilation.models.Building import Building
from HeatAndVentilation.models.Structure import Structure
from HeatAndVentilationCoefficientCalculation.GeometryData.StructuresDataModel import StructureDataModel as d_Structure
from HeatAndVentilationCoefficientCalculation.SpaceData.RoomDataModel import RoomDataModel as d_Room
from HeatAndVentilationCoefficientCalculation.SpaceData.BuildingDataModel import BuildingDataModel as d_Building
from HeatAndVentilationCoefficientCalculation.StaticData.StructureTypeData import StructureTypeData
from HeatAndVentilationCoefficientCalculation.ProjectData.ClimateDataModel import ClimateDataModel as d_ClimateData
import django.db.models


def intersection_structures_list() -> list[str]:
	model_fields = {f.name for f in Structure._meta.get_fields()}
	structure_fields = set(d_Structure.__annotations__.keys())
	return list(set.intersection(structure_fields, model_fields))


def create_room_structure_data_class(structures_list: [django.db.models.QuerySet]):
	all_structures = []
	for structure in structures_list:
		structure_data_class = getattr(StructureTypeData, structure.standard_structure_type).value.class_value(
			structure.name, structure.area, structure.R_custom
		)
		all_structures.append(structure_data_class)
	return all_structures


def serialize_building_data_class(id_: int) -> d_Building:
	building = Building.objects.filter(id=id_).first()
	building_fields = ["building_name", "building_temperature", "heated_volume", "level_number", "level_height", ]
	room_fields = ["category", "room_type", "human_number", "t_in_room", "room_heated_volume", "floor_area_living",
	               "floor_area_heated"]
	climate_data_fields = d_ClimateData.__annotations__.keys()
	room_list = []
	for room in building.rooms.all():
		structures = room.structures_list.all()
		structure_list_data = create_room_structure_data_class(structures)
		room_data = {val: getattr(room, val) for val in room_fields}
		room_data.update({"structures_list": structure_list_data})
		df_room = d_Room(**room_data)
		room_list.append(df_room)

	climate_data = {val: getattr(building.climate_data, val) for val in climate_data_fields if val != "GSOP"}
	d_climate_data = d_ClimateData(**climate_data)
	d_building_data = {val: getattr(building, val) for val in building_fields}
	d_building_data.update({"climate_data": d_climate_data, "rooms": room_list})
	d_building = d_Building(**d_building_data)
	return d_building
