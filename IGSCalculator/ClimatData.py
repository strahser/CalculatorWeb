import pandas as pd
import os
import inspect
import sys



current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from DB.ExcelDBPath import ExcelDBPath
from Utils.Calculation import _filter_df
from GSOPCalculator.Static.GSOPNamesStatic import GSOPNamesStatic
from GSOPCalculator.GSOPModel.CityProperty import CityProperty
from Utils.Render import render_docx


class CalculateGSOPModel:
	def __init__(self, climate_df: pd.DataFrame, city: str):
		_city_data = _filter_df(climate_df, GSOPNamesStatic.city, city)
		self.city_property = CityProperty(
			_city_data[GSOPNamesStatic.t_out].values[0],
			_city_data[GSOPNamesStatic.t_ot_per].values[0],
			_city_data[GSOPNamesStatic.z_ot_per].values[0]
		)


climate_df = pd.read_excel(ExcelDBPath.climate_data)
climate_data = CalculateGSOPModel(climate_df, "Москва")
out_dict = dict(gsop_str=climate_data.city_property.gsop_str,
                t_in=climate_data.city_property.t_in,
                t_out=climate_data.city_property.t_out,
                t_ot_per=climate_data.city_property.t_ot_per,
                z_ot_per=climate_data.city_property.z_ot_per,
                )

template_path = os.path.join(current_dir,"Template", "TemplateIGS.docx")
out_folder = os.path.join(current_dir, "Template")
render_docx(template_path, out_dict, out_folder,doc_name="ИЖС_расчет")
print(out_dict)
from pytexit import py2tex

exprestion = 'Q_heat =c*r*(t1-t2)/550'
py2tex(exprestion)