from enum import Enum


class OrientationData(Enum):
    ND: str = "Нет данных"
    N: str = "С"
    NE: str = "СВ"
    E: str = "В"
    SE: str = "ЮВ"
    S: str = "Ю"
    SW: str = "ЮЗ"
    W: str = "З"
    NW: str = "СЗ"
