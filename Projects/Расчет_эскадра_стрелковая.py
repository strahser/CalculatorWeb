
import os
import inspect
import sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from DetailCalculator.ClassEnergyCalculation import InputData,render_docx,energy_class_calculation
from docxtpl import DocxTemplate
from DB.ExcelDBPath import ExcelDBPath


def calculator_escadra_strelcovay(template_path,out_folder):
    """"подгон класса эн. эф по данным ПЗ"""
    doc = DocxTemplate(template_path)
    class_options = dict(оригинальный=0.092, A=0.29 * 0.5,
                         C=0.29 * 0.8)  # 0.29 справочный коэффициент для нормируемых потерь
    for key in class_options.keys():
        input_data_ = InputData(
            gsop=4811.4,
            q0=class_options[key],
            Vzd=62943,
            Akv=12184.5,
            Apng=104.74 + 332.86,
            Ng=436,
            Nrab=30,
            zot=198,
            q_ee=10
        )
        calc = energy_class_calculation(input_data_, ExcelDBPath.order_399_table1)
        render_docx(doc, calc, out_folder, suffix=f"класс {key}")
template_path = os.path.join(parent_dir,"DetailCalculator", "Энергоэфективность2.docx")
out_folder = os.path.join(root_dir, "Отчеты", "Расчет_эскадра_стрелковая")
calculator_escadra_strelcovay(template_path, out_folder)