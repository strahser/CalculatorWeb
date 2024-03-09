import dataclasses
from StaticDB.models.SunRadiationData import SunRadiationData
from StaticDB.models.ClimateData import ClimateData
from HeatAndVentilation.models.Building import Building
from HeatAndVentilation.models.Room import Room
from HeatAndVentilation.models.BaseStructure import BaseStructure
from HeatAndVentilation.models.Structure import Structure
from StaticDB.models.StandardStructureLayer import StandardStructureLayer
from HeatAndVentilationCoefficientCalculation.Tests.InputData import *


def create_sun_radiation_data():
	sr = SunRadiationData.objects.create()
	print(sr)


def create_climate_data():
	cm = ClimateDataModel()
	cm_dict = dataclasses.asdict(cm)
	cm_dict['sun_radiation'] = SunRadiationData.objects.first()
	cd = ClimateData.objects.create(**cm_dict)
	print(cd)


def create_building():
	c_d = ClimateData.objects.first()
	b = Building.objects.get_or_create(climate_data=c_d)
	print(f"building {b} add to db")


def create_room():
	b = Building.objects.first()
	room = Room.objects.get_or_create(building=b)
	print(f"Room {room} add to db")


def create_base_structures():
	bs_list = [wall_3_16, wall_3_34, wall_3_19, wall_3_42, roof_5_55, roof_4_48, floor_4_46, base_window_0_65,
	           door_0_86]
	for structure in bs_list:
		st_b = BaseStructure.objects.get_or_create(**dataclasses.asdict(structure))
		print(f"structure {st_b} add to db")


def create_structures():
	for struct_data in structures1:
		struct_data_dict = dataclasses.asdict(struct_data)
		bs = BaseStructure.objects.filter(R_real=struct_data.base_structures.R_real).first()
		room_ = Room.objects.first()
		struct_data_dict['base_structures'] = bs
		struct_data_dict['room'] = room_
		st = Structure.objects.get_or_create(**struct_data_dict)
		print(f"structure {st} add to db")


def create_base_structure_layer():
	StandardStructureLayer.objects.create()


def create_all():
	create_sun_radiation_data()
	create_climate_data()
	create_building()
	create_room()
	create_base_structures()
	create_structures()
	create_base_structure_layer()
