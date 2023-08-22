
import os
import inspect
import sys

from Utils.Render import render_docx

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from DetailCalculator.ClassEnergyCalculation import InputData,energy_class_calculation

from docxtpl import DocxTemplate
from DB.ExcelDBPath import ExcelDBPath


def main(template_path,out_folder):
    """"подгон класса эн. эф по данным ПЗ"""

    class_options = dict(оригинальный=0.092, A=0.29 * 0.5,
                         C=0.29 * 0.8)  # 0.29 справочный коэффициент для нормируемых потерь

    input_data_ = InputData(
            Akv=17468,
            Vzd=70048,
            Apng=751,
            Ng=908,
            Nrab=79,
            gsop=4268.4,
            q0= 0.142,
            zot=188,
            q_ee=10
        )
    calc = energy_class_calculation(input_data_, ExcelDBPath.order_399_table1)
    render_docx(template_path, calc, out_folder)
template_path = os.path.join(parent_dir,"DetailCalculator", "HeatTemplate.docx")
out_folder = os.path.join(current_dir, "reports", "base_project_calc")
main(template_path, out_folder)