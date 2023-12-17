import os
import inspect
import sys
import pandas as pd

from IGSCalculator.Models.CalculateGSOPModel import CalculateGSOPModel

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from DB.ExcelDBPath import ExcelDBPath

from Utils.Render import render_docx
climate_df = pd.read_excel(ExcelDBPath.climate_data)
climate_data = CalculateGSOPModel(climate_df, "Москва")
out_dict = dict(gsop_str=climate_data.city_property.gsop_str,
                t_in=climate_data.city_property.t_in,
                t_out=climate_data.city_property.t_out,
                t_ot_per=climate_data.city_property.t_ot_per,
                z_ot_per=climate_data.city_property.z_ot_per,
                )

template_path = os.path.join(root_dir,"Template", "TemplateIGS.docx")
out_folder = os.path.join(root_dir, "Template")
render_docx(template_path, out_dict, out_folder,doc_name="ИЖС_расчет")
print(out_dict)