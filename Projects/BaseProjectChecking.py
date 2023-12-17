import os
import inspect
import sys

from Utils.Render import render_docx

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from DetailCalculator.ClassEnergyCalculation import InputData, energy_class_calculation
from docxtpl import DocxTemplate
from DB.ExcelDBPath import ExcelDBPath


def main(input_data_: InputData, template_path, out_folder, need_render_docx: bool = False):
	""""подгон класса эн. эф по данным ПЗ"""

	class_options = dict(оригинальный=0.092, A=0.29 * 0.5,
	                     C=0.29 * 0.8)  # 0.29 справочный коэффициент для нормируемых потерь

	calc = energy_class_calculation(input_data_, ExcelDBPath.order_399_table1)
	print(calc["n_str"])
	if need_render_docx:
		render_docx(template_path, calc, out_folder)


# region input test
input_data_ = InputData(
	Akv=17468,
	Vzd=70048,
	Apng=751,
	Ng=908,
	Nrab=79,
	gsop=4529,
	q0=0.21,
	zot=188,
	q_ee=10
)
# endregion
# region муниципальное образование Даниловское
input_data2 = InputData(
	level_number=20,
	Akv=9831,
	Vzd=54365,
	Apng=248 + 138,
	Ng=246,
	Nrab=8,
	gsop=4551,
	q0=0.21,
	zot=205,
	q_ee=10
)
"""
МНОГОФУНКЦИОНАЛЬНЫЙ ЖИЛОЙ КОМПЛЕКС С ПОДЗЕМНЫМ ПАРКИНГОМ И
ВСТРОЕННО-ПРИСТРОЕННОЙ ДОО. 1 ЭТАП СТРОИТЕЛЬСТВА
по адресу: г. Москва, внутригородское муниципальное образование Даниловское,
улица Автозаводская, земельный участок 26/1
"""
# endregion


template_path = os.path.join(parent_dir, "DetailCalculator", "HeatTemplate.docx")
out_folder = os.path.join(current_dir, "reports", "base_project_calc")
main(input_data2, template_path, out_folder,True)
