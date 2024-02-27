from dataclasses import dataclass
import numpy as np

from HeatAndVentilationCoefficientCalculation.GeometryData.RoomInterfece import RoomI
from Utils.RenderModel import RenderModel


@dataclass()
class DomesticHeat:
    _room: RoomI

    def _get_domestic_heat_per_square(self):
        """
		где   принимается в соответствии с Г.5 в зависимости от расчетной заселенности
		квартиры по интерполяции между 17вт  при заселенности 20м2  на человека и  10вт при заселенности 45м2  на человека.
				"""
        if self._room.human_number:
            area_for_human = self._room.floor_area_heated / self._room.human_number
            if area_for_human < 20:
                return 17
            elif area_for_human > 45:
                return 10
            else:
                return np.interp(self._room.floor_area_heated, [20, 45], [17, 20])
        else:
            return 0

    def domestic_heat_coefficient(self, building_heated_volume: float, t_in: float, t_ot_middle: float) -> RenderModel:
        """Удельная характеристика бытовых тепловыделений здания"""
        building_temperature_diff = building_heated_volume * (t_in - t_ot_middle)
        output_value = self._get_domestic_heat_per_square() * self._room.floor_area_living / building_temperature_diff
        output_render_value = f"kбыт = {self._get_domestic_heat_per_square()} * {self._room.floor_area_living} / " \
                              f"{building_heated_volume} * ({t_in} - {t_ot_middle}) = {output_value}"
        return RenderModel("Удельная характеристика бытовых тепловыделений здания",
                           output_value=output_value,
                           output_render_value=output_render_value,
                           key="domestic_heat_coefficient")
