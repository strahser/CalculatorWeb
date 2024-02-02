from HeatAndVentilationCoefficientCalculation.SpaceData.Building import Building
from HeatAndVentilationCoefficientCalculation.SpaceData.Room import Room
from HeatAndVentilationCoefficientCalculation.GeometryData.StructuresData import Wall, Roof, Floor, Window, \
	Door
from HeatAndVentilationCoefficientCalculation.StaticData.Category import Category
from HeatAndVentilationCoefficientCalculation.StaticData.OrientationData import OrientationData
from HeatAndVentilationCoefficientCalculation.VentilationCalculation.VentilationCalculationModel import VentilationData
from IGSCalculator.Models.ClimateData import ClimateData

# region Input data
climate_data = ClimateData(
	city_name="Москва",
	t_ot_middle=-3.1,
	t_out_max=-28,
	air_velocity_max=3.8,
	air_velocity_middle=3.8,
	z_ot=216,
	t_in=20
)

structures1 = [
	Wall(name="Навесная фасадная система с основанием из керамзитобетона", short_name="ст1", area=3406, R_real=3.16,
	     ),
	Wall(name="Навесная фасадная система с основанием из железобетона", short_name="ст2", area=608, R_real=3.34,
	     ),
	Wall(name="Трехслойная стена по кладке из керамзитобетона", short_name="ст3", area=1783, R_real=3.19,
	     ),
	Wall(name="Трехслойная стена по монолитному железобетону", short_name="ст3", area=447, R_real=3.42,
	     ),
	Roof(name="Эксплуатируемая кровля", short_name="кр1", area=1296, R_real=5.55,
	     ),
	Roof(name="Совмещенное кровельное покрытие", short_name="кр2", area=339, R_real=4.48,
	     ),
	Floor(name="Перекрытие над проездом", short_name="цок2", area=85, R_real=4.86
	      , ),
	Window(name="Окна", short_name="ок4", area=142, R_real=0.65, orientation=OrientationData.N.name,
	       ),
	Window(name="Окна", short_name="ок4", area=366, R_real=0.65, orientation=OrientationData.NE.name,
	       ),
	Window(name="Окна", short_name="ок4", area=103, R_real=0.65, orientation=OrientationData.E.name,
	       ),
	Window(name="Окна", short_name="ок4", area=286, R_real=0.65, orientation=OrientationData.SE.name,
	       ),
	Window(name="Окна", short_name="ок4", area=67, R_real=0.65, orientation=OrientationData.S.name,
	       ),
	Window(name="Окна", short_name="ок4", area=477, R_real=0.65, orientation=OrientationData.SW.name,
	       ),
	Window(name="Окна", short_name="ок4", area=49, R_real=0.65, orientation=OrientationData.W.name,
	       ),
	Window(name="Окна", short_name="ок4", area=323, R_real=0.65, orientation=OrientationData.NW.name,
	       ),
	Door(name="Входные двери", short_name="дв", area=64, R_real=0.83,
	     ),
]

structures2 = [
	Wall(name="Навесная фасадная система с основанием из керамзитобетона", short_name="ст1", area=503, R_real=3.16,
	     ),
	Wall(name="Навесная фасадная система с основанием из железобетона", short_name="ст2", area=336, R_real=3.34,
	     ),
	Wall(name="Трехслойная стена по кладке из керамзитобетона", short_name="ст3", area=55, R_real=3.19,
	     ),
	Wall(name="Трехслойная стена по монолитному железобетону", short_name="ст3", area=130, R_real=3.42,
	     ),
	Window(name="Окна", short_name="ок", area=430, R_real=0.65, orientation=OrientationData.N.name,
	       ),
]

structures3 = [
	Floor(name="Перекрытие над подвалом", short_name="цок1", area=1550, R_real=1.88,
	      ),
]

structures4 = [
	Window(name="Окна", short_name="ок4", area=142, R_real=0.65, orientation=OrientationData.N.name,
	       ),
	Window(name="Окна", short_name="ок4", area=366, R_real=0.65, orientation=OrientationData.NE.name,
	       ),
	Window(name="Окна", short_name="ок4", area=103, R_real=0.65, orientation=OrientationData.E.name,
	       ),
	Window(name="Окна", short_name="ок4", area=286, R_real=0.65, orientation=OrientationData.SE.name,
	       ),
	Window(name="Окна", short_name="ок4", area=67, R_real=0.65, orientation=OrientationData.S.name,
	       ),
	Window(name="Окна", short_name="ок4", area=477, R_real=0.65, orientation=OrientationData.SW.name,
	       ),
	Window(name="Окна", short_name="ок4", area=49, R_real=0.65, orientation=OrientationData.W.name,
	       ),
	Window(name="Окна", short_name="ок4", area=323, R_real=0.65, orientation=OrientationData.NW.name,
	       ),
]

room1 = Room(human_number=332,
             structures_list=structures1,
             floor_area_living=3793,
             floor_area_heated=13080,
             t_in_room=20,
             category=Category.living.name,
             room_heated_volume=24751,
             room_type="Жилое")
room2 = Room(floor_area_living=1229,
             t_in_room=18,
             category=Category.living.name,
             human_number=3,
             structures_list=structures2,
             room_heated_volume=6303,
             room_type="Жилое")
room3 = Room(floor_area_living=3500,
             t_in_room=8,
             category=Category.living.name,
             structures_list=structures3,
             room_heated_volume=3175,
             room_type="Техническое")
room4 = Room(floor_area_living=3500,
             t_in_room=8,
             category=Category.living.name,
             structures_list=structures4,
             room_heated_volume=3175,
             room_type="Техническое")
building = Building(
	building_name="TEST1",
	climate_data=climate_data,
	heated_volume=34229,
	level_number=20,
	level_height=3,
	rooms=[room1, room2, room3],
	building_temperature=20,

)
building2 = Building(
	building_name="TEST2",
	climate_data=climate_data,
	heated_volume=34229,
	level_number=20,
	level_height=3,
	rooms=[room4],
	building_temperature=20,

)
# endregion
ventilation_data = VentilationData(
	room=room1,
	_climate_data=climate_data,
	_level_height=building.level_height,
	_level_number=building.level_number,
	_building_heated_volume=building.heated_volume,
)
