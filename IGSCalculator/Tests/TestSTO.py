

t_out = -23
t_ot = 4.3
z_ot = 198
t_in = 20
v_air = 1.8
#Из примера НОСТРОЙ
level_number = 1
f_walls = 108
f_windows = 32
f_doors = 2
f_floor = 150
f_roof = 173
f_room_heat = 187
f_room_20c_total = 85  # общая площадь жилых помещений с темп. 20С
f_room_living = 70  # площадь жилых комнат
V_heat = 492  # отапливаемый объем
GSOP = (t_in - t_ot) * z_ot
R_wall_fact: float = 5.06
R_door_fact: float = 1.1
R_window_fact: float = 0.54
R_basement_fact: float = 0.86
R_roof_slab_fact: float = 5.09
r_sum = [R_wall_fact, R_door_fact, R_window_fact, R_basement_fact, R_roof_slab_fact]

