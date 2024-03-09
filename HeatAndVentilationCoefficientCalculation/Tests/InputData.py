from HeatAndVentilationCoefficientCalculation.GeometryData.BaseStructureDataModel import BaseStructureDataModel
from HeatAndVentilationCoefficientCalculation.GeometryData.StructuresDataModel import StructureDataModel
from HeatAndVentilationCoefficientCalculation.SpaceData.BuildingDataModel import BuildingDataModel
from HeatAndVentilationCoefficientCalculation.SpaceData.RoomDataModel import RoomDataModel
from HeatAndVentilationCoefficientCalculation.StaticData.RoomCategory import RoomCategory
from HeatAndVentilationCoefficientCalculation.StaticData.OrientationData import OrientationData
from HeatAndVentilationCoefficientCalculation.StaticData.StructureTypeData import StructureTypeData
from HeatAndVentilationCoefficientCalculation.VentilationCalculation.VentilationCalculationModel import VentilationData
from HeatAndVentilationCoefficientCalculation.ProjectData.ClimateDataModel import ClimateDataModel

# region Input data
climate_data = ClimateDataModel(
	name="Москва",
	t_ot_middle=-3.1,
	t_out_max=-28,
	air_velocity_max=3.8,
	air_velocity_middle=3.8,
	z_ot=216,
)

# region Базовые конструкции

wall_3_16 = BaseStructureDataModel(name="Навесная фасадная система с основанием из керамзитобетона", R_real=3.16,
                                   standard_structure_type=StructureTypeData.Wall.name)
wall_3_34 = BaseStructureDataModel(name="Навесная фасадная система с основанием из железобетона", R_real=3.34,
                                   standard_structure_type=StructureTypeData.Wall.name)
wall_3_19 = BaseStructureDataModel(name="Трехслойная стена по кладке из керамзитобетона", R_real=3.19,
                                   standard_structure_type=StructureTypeData.Wall.name)
wall_3_42 = BaseStructureDataModel(name="Трехслойная стена по монолитному железобетону", R_real=3.42,
                                   standard_structure_type=StructureTypeData.Wall.name)
roof_5_55 = BaseStructureDataModel(name="Эксплуатируемая кровля", R_real=5.55,
                                   standard_structure_type=StructureTypeData.Roof.name)
roof_4_48 = BaseStructureDataModel(name="Совмещенное кровельное покрытие", R_real=4.48,
                                   standard_structure_type=StructureTypeData.Roof.name)
floor_4_46 = BaseStructureDataModel(name="Перекрытие над проездом", R_real=4.86,
                                    standard_structure_type=StructureTypeData.Floor.name)
base_window_0_65 = BaseStructureDataModel(name="стандартное окно", R_real=0.65,
                                          standard_structure_type=StructureTypeData.Window.name)
door_0_86 = base_structures = BaseStructureDataModel(name="Входная дверь", R_real=0.83,
                                                     standard_structure_type=StructureTypeData.Door.name)

# endregion


structures1 = [
	StructureDataModel(name=wall_3_16.name, short_name="ст1", area=3406, base_structures=wall_3_16),
	StructureDataModel(name=wall_3_34.name, short_name="ст2", area=608, base_structures=wall_3_34),
	StructureDataModel(name=wall_3_19.name, short_name="ст3", area=1783, base_structures=wall_3_19),
	StructureDataModel(name=wall_3_42.name, short_name="ст3", area=447, base_structures=wall_3_42),
	StructureDataModel(name=roof_5_55.name, short_name="кр1", area=1296, base_structures=roof_5_55),
	StructureDataModel(name=roof_4_48.name, short_name="кр2", area=339, base_structures=roof_4_48),
	StructureDataModel(name=floor_4_46.name, short_name="цок2", area=85, base_structures=floor_4_46),

	StructureDataModel(name=base_window_0_65.name,
	                   short_name="ок4", area=142,
	                   base_structures=base_window_0_65,
	                   orientation=OrientationData.N.name
	                   ),
	StructureDataModel(name=base_window_0_65.name,
	                   short_name="ок4", area=366,
	                   base_structures=base_window_0_65,
	                   orientation=OrientationData.NE.name
	                   ),
	StructureDataModel(name=base_window_0_65.name,
	                   short_name="ок4", area=103,
	                   base_structures=base_window_0_65,
	                   orientation=OrientationData.E.name
	                   ),
	StructureDataModel(name=base_window_0_65.name,
	                   short_name="ок4", area=286,
	                   base_structures=base_window_0_65,
	                   orientation=OrientationData.SE.name
	                   ),
	StructureDataModel(name=base_window_0_65.name,
	                   short_name="ок4", area=67,
	                   base_structures=base_window_0_65, orientation=OrientationData.S.name
	                   ),
	StructureDataModel(name=base_window_0_65.name,
	                   short_name="ок4", area=477,
	                   base_structures=base_window_0_65, orientation=OrientationData.SW.name)
	,
	StructureDataModel(name=base_window_0_65.name,
	                   short_name="ок4", area=49, base_structures=base_window_0_65,
	                   orientation=OrientationData.W.name
	                   ),
	StructureDataModel(name=base_window_0_65.name,
	                   short_name="ок4", area=323, base_structures=base_window_0_65,
	                   orientation=OrientationData.NW.name
	                   ),
	StructureDataModel(name=door_0_86.name,
	                   short_name="дв", area=64, base_structures=door_0_86
	                   ),
]

room1 = RoomDataModel(name="Помещение1",
                      human_number=332,
                      structures_list=structures1,
                      floor_area_living=3793,
                      floor_area_heated=13080,
                      t_in_room=18,
                      category=RoomCategory.living.name,
                      room_heated_volume=24751,
                      )

building = BuildingDataModel(
	name="TEST1",
	climate_data=climate_data,
	category='living',
	heated_volume=34229,
	level_number=20,
	level_height=3,
	rooms=[room1],
	building_temperature=20,
)

ventilation_data = VentilationData(
	room=room1,
	_climate_data=climate_data,
	_level_height=building.level_height,
	_level_number=building.level_number,
	_building_heated_volume=building.heated_volume,
)

# structures2 = [
# 	StructureDataModel(name="Навесная фасадная система с основанием из керамзитобетона",
# 	                   short_name="ст1", area=503, r_real=3.16, standard_structure_type=StructureTypeData.Wall.name
# 	                   ),
# 	StructureDataModel(name="Навесная фасадная система с основанием из железобетона",
# 	                   short_name="ст2", area=336, r_real=3.34, standard_structure_type=StructureTypeData.Wall.name
# 	                   ),
# 	StructureDataModel(name="Трехслойная стена по кладке из керамзитобетона",
# 	                   short_name="ст3", area=55, r_real=3.19, standard_structure_type=StructureTypeData.Wall.name
# 	                   ),
# 	StructureDataModel(name="Трехслойная стена по монолитному железобетону",
# 	                   short_name="ст3", area=130, r_real=3.42, standard_structure_type=StructureTypeData.Wall.name
# 	                   ),
# 	StructureDataModel(name=base_window_0_65.name,
# 	                   short_name="ок", area=430, r_real=0.65, orientation=OrientationData.N.name,
# 	                   standard_structure_type=StructureTypeData.Window.name
# 	                   ),
# ]
#
# structures3 = [
# 	StructureDataModel(name="Перекрытие над подвалом",
# 	                   short_name="цок1", area=1550, r_real=1.88,
# 	                   standard_structure_type=StructureTypeData.Wall.name
# 	                   ),
# ]
#
# structures4 = [
# 	StructureDataModel(name=base_window_0_65.name,
# 	                   short_name="ок4", area=142, r_real=0.65, orientation=OrientationData.N.name,
# 	                   standard_structure_type=StructureTypeData.Window.name
# 	                   ),
#
# 	StructureDataModel(name=base_window_0_65.name,
# 	                   short_name="ок4", area=366, r_real=0.65, orientation=OrientationData.NE.name,
# 	                   standard_structure_type=StructureTypeData.Window.name
# 	                   ),
#
# 	StructureDataModel(name=base_window_0_65.name,
# 	                   short_name="ок4", area=103, r_real=0.65, orientation=OrientationData.E.name,
# 	                   standard_structure_type=StructureTypeData.Window.name
# 	                   ),
#
# 	StructureDataModel(name=base_window_0_65.name,
# 	                   short_name="ок4", area=286, r_real=0.65, orientation=OrientationData.SE.name,
# 	                   standard_structure_type=StructureTypeData.Window.name
# 	                   ),
#
# 	StructureDataModel(name=base_window_0_65.name,
# 	                   short_name="ок4", area=67, r_real=0.65, orientation=OrientationData.S.name,
# 	                   standard_structure_type=StructureTypeData.Window.name
# 	                   ),
#
# 	StructureDataModel(name=base_window_0_65.name,
# 	                   short_name="ок4", area=477, r_real=0.65, orientation=OrientationData.SW.name,
# 	                   standard_structure_type=StructureTypeData.Window.name
# 	                   ),
#
# 	StructureDataModel(name=base_window_0_65.name,
# 	                   short_name="ок4", area=49, r_real=0.65, orientation=OrientationData.W.name,
# 	                   standard_structure_type=StructureTypeData.Window.name
# 	                   ),
#
# 	StructureDataModel(name=base_window_0_65.name,
# 	                   short_name="ок4", area=323, r_real=0.65, orientation=OrientationData.NW.name,
# 	                   standard_structure_type=StructureTypeData.Window.name
# 	                   ),
#
# ]
# room2 = RoomDataModel(name="Помещение2",
#                       floor_area_living=1229,
#                       t_in_room=18,
#                       category=RoomCategory.living.name,
#                       human_number=3,
#                       structures_list=structures2,
#                       room_heated_volume=6303,
#                       )
#
# room3 = RoomDataModel(name="Помещение3",
#                       floor_area_living=3500,
#                       t_in_room=8,
#                       category=RoomCategory.living.name,
#                       structures_list=structures3,
#                       room_heated_volume=3175,
#                       )
#
# room4 = RoomDataModel(name="Помещение4",
#                       floor_area_living=3500,
#                       t_in_room=8,
#                       category=RoomCategory.living.name,
#                       structures_list=structures4,
#                       room_heated_volume=3175,
#                       )


# building2 = BuildingDataModel(
# 	name="TEST2",
# 	climate_data=climate_data,
# category='living',
# 	heated_volume=34229,
# 	level_number=20,
# 	level_height=3,
# 	rooms=[room4],
# 	building_temperature=20,

# )
# endregion
