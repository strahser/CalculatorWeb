
from pprint import pprint

from HeatAndVentilationCoefficientCalculation.Tests.InputData import structures1, ventilation_data, building, room1, \
	climate_data, building2
from HeatAndVentilationCoefficientCalculation.VentilationCalculation.WindowInfiltration import WindowInfiltration
from HeatAndVentilationCoefficientCalculation.HeatCalculation.DomesticHeat import DomesticHeat
from HeatAndVentilationCoefficientCalculation.HeatCalculation.SunRadiationHeat import SunRadiationData

ventilation_data.get_building_local_ventilation_coefficient()
building.get_building_structure_heat_resistence_total_coefficient_local()
building.get_building_domestic_heat_coefficient()
building.get_building_ventilation_coefficient()
building.get_building_local_heating_and_ventilation_coefficient(SunRadiationData)
infiltration = WindowInfiltration(22.1, -3.1, 18, 3.8)
infiltration.g_inf_window(244)
domestic_heat = DomesticHeat(room1)
domestic_heat.domestic_heat_coefficient(building_heated_volume=building.heated_volume, t_in=20,
                                        t_ot_middle=climate_data.t_ot_middle)
pprint(structures1.get_structure_heat_resistence_total_coefficient())
pprint(building.get_building_local_heating_and_ventilation_coefficient(SunRadiationData))
pprint(structures1.get_structure_heat_resistence_total_coefficient())
pprint(structures1.get_structure_heat_resistence_total_coefficient_local())
radiation = building2.get_building_sun_radiation_coefficient(SunRadiationData)
