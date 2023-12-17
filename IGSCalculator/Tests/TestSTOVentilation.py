#region Test
from HeatAndVentilationCoefficientCalculation.VentilationCalculation.VentilationCalculationUtility import delta_pressure_window, delta_pressure_door, G_inf, n_vent, L_vent

Area_living = 10330
human_number = 413
height_building = 76
air_velocity_max = 4.9
air_velocity_mid = 3.8
t_out = -28
t_in = 18
t_midl_heat = -3.1
window_area = 63
door_area = 18

c_air = 1.006  # теплоемкость воздуха
l_vent = L_vent(Area_living, human_number)
d_pressure_window = delta_pressure_window(height_building, t_in, t_out, air_velocity_max)
d_pressure_door = delta_pressure_door(height_building, t_in, t_out, air_velocity_max)
d_pressure_window_mid = delta_pressure_window(height_building, t_in, t_midl_heat, air_velocity_max)
d_pressure_door_mid = delta_pressure_door(height_building, t_in, t_midl_heat, air_velocity_mid)
g_inf = G_inf(window_area, door_area, height_building, t_in, t_out, air_velocity_max, R_u_window=0.9, R_u_door=0.14)
n_vent = n_vent(Area_living, l_vent, g_inf)
print(n_vent)
#endregion