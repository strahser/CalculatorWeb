from pprint import pprint

from HeatAndVentilationCoefficientCalculation.AreasData.Building import Building
from HeatAndVentilationCoefficientCalculation.AreasData.Room import Room
from HeatAndVentilationCoefficientCalculation.GeometryData.StructuresData import Structures, Wall, Roof, Floor, Window, \
	Door
from HeatAndVentilationCoefficientCalculation.HeatCalculation.DomesticHeat import DomesticHeat
from HeatAndVentilationCoefficientCalculation.HeatCalculation.SunRadiationHeat import SunRadiationData
from HeatAndVentilationCoefficientCalculation.StaticData.Category import Category
from HeatAndVentilationCoefficientCalculation.StaticData.OrientationData import OrientationData
from HeatAndVentilationCoefficientCalculation.VentilationCalculation.VentilationCalculationModel import VentilationData
from HeatAndVentilationCoefficientCalculation.VentilationCalculation.WindowInfiltration import WindowInfiltration
from IGSCalculator.Models.ClimateData import ClimateData

# region Input data
climate_data = ClimateData(
	t_ot_middle=-3.1,
	t_out_max=-28,
	air_velocity_max=3.8,
	air_velocity_middle=3.8,
	z_ot=216,
	t_in=20
)

structures1 = Structures(
	[Wall(name="Навесная фасадная система с основанием из керамзитобетона", short_name="ст1", area=3406, R_real=3.16,
	      gsop=climate_data.GSOP),
	 Wall(name="Навесная фасадная система с основанием из железобетона", short_name="ст2", area=608, R_real=3.34,
	      gsop=climate_data.GSOP),
	 Wall(name="Трехслойная стена по кладке из керамзитобетона", short_name="ст3", area=1783, R_real=3.19,
	      gsop=climate_data.GSOP),
	 Wall(name="Трехслойная стена по монолитному железобетону", short_name="ст3", area=447, R_real=3.42,
	      gsop=climate_data.GSOP),
	 Roof(name="Эксплуатируемая кровля", short_name="кр1", area=1296, R_real=5.55,
	      gsop=climate_data.GSOP),
	 Roof(name="Совмещенное кровельное покрытие", short_name="кр2", area=339, R_real=4.48,
	      gsop=climate_data.GSOP),

	 Floor(name="Перекрытие над проездом", short_name="цок2", area=85, R_real=4.86
	       ,gsop=climate_data.GSOP),
	 # Window(name="Окна", short_name="ок", area=1383, R_real=0.65)

	 Window(name="Окна", short_name="ок4", area=142, R_real=0.65, orientation=OrientationData.N.name,
	        gsop=climate_data.GSOP),
	 Window(name="Окна", short_name="ок4", area=366, R_real=0.65, orientation=OrientationData.NE.name,
	        gsop=climate_data.GSOP),
	 Window(name="Окна", short_name="ок4", area=103, R_real=0.65, orientation=OrientationData.E.name,
	        gsop=climate_data.GSOP),
	 Window(name="Окна", short_name="ок4", area=286, R_real=0.65, orientation=OrientationData.SE.name,
	        gsop=climate_data.GSOP),
	 Window(name="Окна", short_name="ок4", area=67, R_real=0.65, orientation=OrientationData.S.name,
	        gsop=climate_data.GSOP),
	 Window(name="Окна", short_name="ок4", area=477, R_real=0.65, orientation=OrientationData.SW.name,
	        gsop=climate_data.GSOP),
	 Window(name="Окна", short_name="ок4", area=49, R_real=0.65, orientation=OrientationData.W.name,
	        gsop=climate_data.GSOP),
	 Window(name="Окна", short_name="ок4", area=323, R_real=0.65, orientation=OrientationData.NW.name,
	        gsop=climate_data.GSOP),
	 Door(name="Входные двери", short_name="дв", area=64, R_real=0.83,
	      gsop=climate_data.GSOP),
	 ]
)
structures2 = Structures(
	[Wall(name="Навесная фасадная система с основанием из керамзитобетона", short_name="ст1", area=503, R_real=3.16,
	      gsop=climate_data.GSOP),
	 Wall(name="Навесная фасадная система с основанием из железобетона", short_name="ст2", area=336, R_real=3.34,
	      gsop=climate_data.GSOP),
	 Wall(name="Трехслойная стена по кладке из керамзитобетона", short_name="ст3", area=55, R_real=3.19,
	      gsop=climate_data.GSOP),
	 Wall(name="Трехслойная стена по монолитному железобетону", short_name="ст3", area=130, R_real=3.42,
	      gsop=climate_data.GSOP),
	 Window(name="Окна", short_name="ок", area=430, R_real=0.65, orientation=OrientationData.N.name,gsop=climate_data.GSOP),
	 ]
)
structures3 = Structures(
	[
		Floor(name="Перекрытие над подвалом", short_name="цок1", area=1550, R_real=1.88,
		      gsop=climate_data.GSOP),
	]
)
structures4 = Structures(
	[
		Window(name="Окна", short_name="ок4", area=142, R_real=0.65, orientation=OrientationData.N.name,
		       gsop=climate_data.GSOP),
		Window(name="Окна", short_name="ок4", area=366, R_real=0.65, orientation=OrientationData.NE.name,
		       gsop=climate_data.GSOP),
		Window(name="Окна", short_name="ок4", area=103, R_real=0.65, orientation=OrientationData.E.name,
		       gsop=climate_data.GSOP),
		Window(name="Окна", short_name="ок4", area=286, R_real=0.65, orientation=OrientationData.SE.name,
		       gsop=climate_data.GSOP),
		Window(name="Окна", short_name="ок4", area=67, R_real=0.65, orientation=OrientationData.S.name,
		       gsop=climate_data.GSOP),
		Window(name="Окна", short_name="ок4", area=477, R_real=0.65, orientation=OrientationData.SW.name,
		       gsop=climate_data.GSOP),
		Window(name="Окна", short_name="ок4", area=49, R_real=0.65, orientation=OrientationData.W.name,
		       gsop=climate_data.GSOP),
		Window(name="Окна", short_name="ок4", area=323, R_real=0.65, orientation=OrientationData.NW.name,
		       gsop=climate_data.GSOP),
	]
)

room1 = Room(human_number=332,
             structures=structures1,
             floor_area_living=3793,
             floor_area_heated=13080,
             t_in_room=20,
             t_in_building=climate_data.t_in,
             t_ot=climate_data.t_ot_middle,
             category=Category.living,
             room_heated_volume=24751,
             room_type="Жилое")
room2 = Room(floor_area_living=1229,
             t_in_room=18,
             t_in_building=climate_data.t_in,
             t_ot=climate_data.t_ot_middle,
             category=Category.living,
             human_number=3,
             structures=structures2,
             room_heated_volume=6303,
				room_type="Жилое")
room3 = Room(floor_area_living=3500,
             t_in_room=8,
             t_in_building=climate_data.t_in,
             t_ot=climate_data.t_ot_middle,
             category=Category.living,
             structures=structures3,
             room_heated_volume=3175,
             room_type="Техническое")
room4 = Room(floor_area_living=3500,
             t_in_room=8,
             t_in_building=climate_data.t_in,
             t_ot=climate_data.t_ot_middle,
             category=Category.living,
             structures=structures4,
             room_heated_volume=3175,
             room_type="Техническое")
building = Building(
	climate_data=climate_data,
	heated_volume=34229,
	level_number=20,
	level_height=3,
	rooms=[room1, room2, room3],
	building_temperature=20,

)
building2 = Building(
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
# pprint(structures1.get_structure_heat_resistence_total_coefficient())
# ventilation_data.get_building_local_ventilation_coefficient()
# building.get_building_structure_heat_resistence_total_coefficient_local()
# building.get_building_domestic_heat_coefficient()
# building.get_building_ventilation_coefficient()
# building.get_building_local_heating_and_ventilation_coefficient(SunRadiationData)
# infiltration = WindowInfiltration(22.1, -3.1, 18, 3.8)
# infiltration.g_inf_window(244)
# domestic_heat = DomesticHeat(room1)
# domestic_heat.domestic_heat_coefficient(building_heated_volume=building.heated_volume, t_in=20,
#                                         t_ot_middle=climate_data.t_ot_middle)
# pprint(building.get_building_local_heating_and_ventilation_coefficient(SunRadiationData))
# pprint(structures1.get_structure_heat_resistence_total_coefficient())
# pprint(structures1.get_structure_heat_resistence_total_coefficient_local())
# radiation = building2.get_building_sun_radiation_coefficient(SunRadiationData)
