from pprint import pprint

import pandas as pd

from HeatAndVentilationCoefficientCalculation.StaticData.SunRadiationHeat import SunRadiationHeat
from HeatAndVentilationCoefficientCalculation.Tests.InputData import building, structures1

pprint(building.get_building_total_structure_area())
pprint(building.get_building_structure_heat_resistence_total_coefficient())
pprint(building.get_normative_building_structure_heat_resistence_total_coefficient())
pprint(building.get_building_compact_coefficient())
pprint(building.get_building_structure_heat_resistence_total_coefficient_local())
pprint(building.get_building_sun_radiation_coefficient(SunRadiationHeat))
pprint(building.get_building_ventilation_coefficient())
pprint(building.get_building_domestic_heat_coefficient())
pprint(building.get_building_local_heating_and_ventilation_coefficient(SunRadiationHeat))
building.update_room_coefficient()
pprint([room.n_temperature_coefficient for room in building.rooms])
pprint(*[[structure.n_temperature_coefficient for structure in room.structures_list] for room in building.rooms])
