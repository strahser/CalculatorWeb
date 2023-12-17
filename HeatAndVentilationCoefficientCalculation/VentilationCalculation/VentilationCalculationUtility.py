from Utils.RenderModel import RenderModel


def air_viscosity(temperature):
	return 353 / (273 + temperature)


def air_local_mass(temperature):
	return 3463 / (273 + temperature)


def delta_pressure_window(height_building, t_in, t_out, air_velocity):
	"""
    требуемое сопротивление воздухопроницанию окон и балконных дверей и входных наружных дверей,
    """
	r_out = air_local_mass(t_out)
	r_in = air_local_mass(t_in)
	delta_pressure = 0.28 * height_building * (r_out - r_in) + 0.03 * r_out * air_velocity ** 2
	return delta_pressure


def delta_pressure_door(height_building, t_in, t_out, air_velocity):
	"""

    требуемое сопротивление воздухопроницанию окон и балконных дверей и входных наружных дверей,
    """
	r_out = air_local_mass(t_out)
	r_in = air_local_mass(t_in)
	delta_pressure = 0.55 * height_building * (r_out - r_in) + 0.03 * r_out * air_velocity ** 2
	return delta_pressure


def window_air_resistence(height_building, t_in, t_out, air_velocity):
	return delta_pressure_window(height_building, t_in, t_out, air_velocity) / 6


def G_inf(window_area, door_area, height_building, t_in, t_out, air_velocity, R_u_window=0.9, R_u_door=0.14) -> float:
	"""
    Г.4 Количество инфильтрующегося воздуха, поступающего в лестничную клетку жилого здания
    или в помещения общественного здания через неплотности заполнений проемов, полагая, что все они
     находятся на наветренной стороне, следует определять по формуле
    0,47 м2∙ч/кг – для одинарной двери;26
     0,7 м2∙ч/кг – для двойных дверей с тамбуром;
    0,85 м2∙ч/кг – для тройных дверей с двумя тамбурами между ними.
    Rинф.вх.дв – сопротивление воздухопроницанию входных дверей или ворот,м2∙ч/кг; принимают при ∆Pо = 10 Па:
    – 0,14 м2∙ч/кг – для входов в жилые здания, предприятия торговли и др.
    объекты с массовым проходом людей;
    – 0,16 м2∙ч/кг – для жилых зданий повышенной комфортности;
    – 0,14 м2∙ч/кг – для вращающихся дверей с тремя перегородками;
    – 0,16 м2∙ч/кг – для вращающихся дверей с четырьмя перегородками;
    """
	d_p_window_10_pa = (delta_pressure_window(height_building, t_in, t_out, air_velocity) / 10) ** 2 / 3
	d_p_door_10_pa = (delta_pressure_door(height_building, t_in, t_out, air_velocity) / 10) ** 1 / 2
	g_inf_window = (window_area * d_p_window_10_pa / R_u_window)
	g_inf_door = (door_area * d_p_door_10_pa / R_u_door)
	f"{g_inf_window} = ({window_area}* {d_p_window_10_pa}/{R_u_window})"
	return g_inf_window + g_inf_door






