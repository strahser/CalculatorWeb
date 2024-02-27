# region importsys
from __future__ import division
import os
from dataclasses import dataclass
import locale
import pandas as pd
locale.setlocale(locale.LC_ALL, '')
locale.currency(1234567.89, grouping=True)

from EnergyCompare.Process.DataTableInterpolation import DataTableInterpolation


# endregion

# region input
@dataclass
class InputDataLabel:
    """Исходные обозначения обязательные - ГСОП,Площади, количества этажей, нагрузка на отопление вентиляцию"""
    gsop: str = "Градусо-сутки отопительного периода"
    q0: str = "Расчётная характеристика расхода тепловой энергии на отопление и вентиляцию кВт∙ч/м2"
    Vzd: str = "Отапливаемый объём здания м3"
    level_number: str = "Количество этажей"
    Akv: str = "Площадь квартир жилого здания, кв.м"
    Apng: str = "Полезная площадь нежилых помещений, кв.м"
    Ng: str = "Количество жителей в здании, чел."
    Nrab: str = "Количество работающих в нежилых помещениях здания, чел."
    alfa: float = "коэффициент, учитывающий снижение горячего водопотребления в летний период для МКД"
    zot: str = "Продолжительность отопительного периода со средней суточной температурой воздуха ниже или равной 8 гр. сут"
    Kef_gvs: str = "Коэффициент эффективности использования ГВС"
    q_ee: str = """
    базовый удельный годовой расход электрической энергии на общедомовые нужды оборудованных лифтом"""


@dataclass
class InputData:
    """Исходные данные обязательные - ГСОП,Площади, количества этажей, нагрузка на отопление вентиляцию"""
    gsop: float = 4271.0  # для 20 градусов температуры внутреннего воздуха, Калининград
    q0: float = 0.142  # Расчётная характеристика расхода тепловой энергии на отопление и вентиляцию
    Vzd: float = 70048  # Отапливаемый объём здания
    level_number: int = 24  # Количество этажей
    Akv: float = 17468  # Площадь квартир жилого здания
    Apng: float = 751  # Полезная площадь нежилых помещений жилого здания
    Ng: int = 908  # Количество жителей жилого здания
    Nrab: int = 79  # Количество работающих в нежилых помещениях
    alfa: float = 0.9
    zot: int = 193  # количество дней отопительного периода
    Kef_gvs: float = 0.64  # Коэффициент эффективности использования ГВС
    q_ee: float = 10  # Удельный годовой расход электрической энергии на общедомовые нужды МКД, оборудованных лифтом


def round_format(data, acc=1):
    return '{:,.2f}'.format(round(data, acc)).replace(",", " ")


# endregion




def get_base_q_value(gsop: float, level_number: int, path_to_excel_table_order_399_table1: str):
    """определение годового потребления тепла для расчета класса ээ согласно пп 339 РФ"""
    df = pd.read_excel(path_to_excel_table_order_399_table1)
    interpolation = DataTableInterpolation(df)
    base_value = interpolation.interpolate_df(gsop, level_number).values.flatten()[0]
    return base_value


def get_energy_class(data_value):
    """Согласно пп 339 РФ"""
    if data_value <= -60:
        return "A++"
    elif -50 >= data_value > -60:
        return "A+"
    elif -40 >= data_value > -50:
        return "A"
    elif -30 >= data_value > -40:
        return "B"
    elif -15 >= data_value > -30:
        return "C"
    elif -15 <= data_value < 0:
        return "D"
    elif 0 <= data_value < 25:
        return "E"
    elif 25 <= data_value < 50:
        return "F"
    elif data_value >= 50:
        return "G"


def create_input_render_dictionary(input_data: InputData) -> dict[str, float]:
    """Соединение обозначения и значений обязательных исходнных данных для рендера ПЗ"""
    inp_values = [getattr(input_data, val) for val in input_data.__annotations__.keys()]
    label_values = [f"{en}. {getattr(InputDataLabel, val)}" for en, val in
                    enumerate(InputDataLabel.__annotations__.keys(), 1)]
    input_dict = dict(zip(label_values, inp_values))
    input_dict_out = "\n".join([f"{key} = {val}" for key, val in input_dict.items()])
    return input_dict_out


def energy_class_calculation(input_data: InputData, path_to_excel_table_order_399_table1):
    # region InputData
    """
    Исходные данные для рендера пояснительной записки
    """
    gsop: float = input_data.gsop  # для 20 градусов температуры внутреннего воздуха,
    q0: float = input_data.q0  # !!!Расчётная характеристика расхода тепловой энергии на отопление и вентиляцию
    Vzd: float = input_data.Vzd  # Отапливаемый объём здания
    level_number: int = input_data.level_number  # Количество этажей
    Akv: float = input_data.Akv  # Площадь квартир жилого здания
    Apng: float = input_data.Apng  # Полезная площадь нежилых помещений жилого здания
    Ng: int = input_data.Ng  # Количество жителей жилого здания
    Nrab: int = input_data.Nrab  # Количество работающих в нежилых помещениях
    alfa: float = input_data.alfa  # Полезная площадь нежилых помещений жилого здания
    zot: int = input_data.zot  # количество дней отопительного периода
    Kef_gvs: float = input_data.Kef_gvs  # Коэффициент эффективности использования ГВС
    q_ee: float = input_data.q_ee  # Удельный годовой расход электрической энергии на общедомовые нужды МКД, оборудованных лифтом
    input_dict_out = create_input_render_dictionary(input_data=input_data)
    V_gv = 70#Расчетный нормативный среднесуточный расход горячей воды на человека vгв, л/(сут*чел)
    #- с ваннами длиной от 1500 мм, оборудованными душами
    # endregion
    # region EnergyCalculation
    """ Определяем базовое значение энергопотребления"""
    q_base = get_base_q_value(gsop, level_number, path_to_excel_table_order_399_table1)
    """
    Расход тепловой энергии на отопление и вентиляцию здания за отопительный
    период Q_от^год, кВт·ч/год, следует определять по формуле
    """
    Qgod_ot = 0.024 * gsop * Vzd * q0
    Qgod_ot_str = f"0.024*{round_format(gsop)}*{round_format(Vzd)}*{q0} = {round_format(Qgod_ot)}"
    """    
    Опеределяем Удельный годовой расход тепловой энергии на отопление и вентиляцию МКД, кВт∙ч/м2:
    """
    qot = round(Qgod_ot / (Akv + Apng), 2)
    qot_str = f"{round_format(Qgod_ot)}/({Akv}+{Apng})= {round_format(qot)}"
    """
    Определяем среднесуточный расход горячей воды для квартир МКД за сутки, м3/сут:
    """
    Vgv_g = round(V_gv * Ng * 0.001 * ((zot + alfa * (355 - zot)) / 365), 2)
    Vgv_g_str = f"{V_gv}*{Ng}*0.001*(({zot}+{alfa}*(355-{zot}))/365) = {round_format(Vgv_g)}"
    """
    Определяем среднесуточный расход горячей воды для нежилой части МКД за сутки, м3/сут:
    """
    Vgv_ng = round(5.1 * Nrab * 0.001 * (zot + 0.5 * (355 - zot)) / 365, 2)
    Vgv_ng_str = f"5.1*{Nrab}*0.001*({zot}+0.5*(355-{zot}))/365= {round_format(Vgv_ng)}"
    """
    Общий Среднесуточный расход горячей воды для МКД, м3/сут определяем:
    """
    Vgv = round(Vgv_g) + round(Vgv_ng)
    Vgv_str = f"{round_format(Vgv_g)}+ {round_format(Vgv_ng)}={round_format(Vgv)}"
    """
    Величина годового расхода тепловой энергии на горячее водоснабжение МКД, МВт∙ч:
    """
    Qgv = round(1.17 * Vgv * 55 * (355 * 0.15 + zot + (alfa * 0.9 * (365 - 10 - zot)) * 45 / 55) * Kef_gvs, 2)
    Qgv_str = f"""
    1.17*{round_format(Vgv)}*55*(355*0.15+{zot}+({alfa}*0.9*(365-10-{zot})*45/55)*{Kef_gvs}= {round_format(Qgv)}
    """
    """
    Удельный годовой расход тепловой энергии на горячее водоснабжение МКД, кВт∙ч/м2:
    """
    q_gv = round(Qgv / (Akv + Apng))
    q_gv_str = f"{round_format(Qgv)}/({Akv} + {Apng})= {round_format(q_gv)}"
    """
    Суммарный удельный годовой расхода энергетических ресурсов МКД.
    """
    q_sum = round(qot + q_gv + q_ee, 2)
    q_sum_str = f"{qot}+{q_gv}+{q_ee}= {round_format(q_sum)}"
    """
    Относительное отклонение показателя 
    суммарного удельного годового расхода энергетических ресурсов от базовых значений
    """
    n = ((q_sum - q_base) / q_base) * 100
    class_ee = (get_energy_class(n))
    n_str = f"""((n= {round_format(q_sum)}-{q_base})/{q_base})*100= {round_format(n)} 
    что соответсвует классу энергоэффективности {class_ee}    
    """
    # endregion
    short_context = dict(
        input_dict_out=input_dict_out,
        V_gv= V_gv,
        Qgod_ot_str=Qgod_ot_str,
        qot_str=qot_str,
        Vgv_g_str=Vgv_g_str,
        Vgv_ng_str=Vgv_ng_str,
        Vgv_str=Vgv_str,
        q_gv_str=q_gv_str,
        q_sum=q_sum,
        q_sum_str=q_sum_str,
        Qgv_str=Qgv_str,
        q_base=q_base,
        q_ee=q_ee,
        n_str=n_str,
    )

    return short_context
