from pprint import pprint

import pandas as pd
from HeatAndVentilationCoefficientCalculation.Tests.Test import building
import os
import inspect
import sys

from Utils.Render import render_docx

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)

f_sum = "\n".join((f"F{en + 1}=" + val.output_render_value + "м2" for en, val in
                   enumerate(building.get_building_total_structure_area().output_render_list)))
F_total = f"{building.get_building_total_structure_area().output_value}"

# pprint(building.all_structures)
df = pd.DataFrame(building.all_structures)
df.loc["Total"] = df[['_n_temperature_koef', 'area', 'a_r_n', 'percent_a_r_n']].sum()
df = df.fillna("-").round(2)
filter_columns = ['name', '_n_temperature_koef', 'area', 'R_real', 'a_r_n', 'percent_a_r_n']
df = df[filter_columns]
k_total = building.get_building_structure_heat_resistence_total_coefficient_local().output_value

out_dictionary = dict(f_sum= f_sum, F_total= F_total, df= df,k_total = k_total)
template_path = os.path.join(parent_dir, "Templates", "Q_heat_and_ventilation_template.docx")
out_folder = os.path.join(current_dir, "reports")
render_docx(template_path=template_path, short_context=out_dictionary, out_folder=out_folder, doc_name="base_data.docx")