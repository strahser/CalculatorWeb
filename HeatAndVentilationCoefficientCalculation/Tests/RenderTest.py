from pprint import pprint
import os
import inspect
import sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from HeatAndVentilationCoefficientCalculation.Tests.InputData import building
from HeatAndVentilationCoefficientCalculation.RenderData.RenderData import render_data
from Utils.Render import render_docx

short_context = render_data(building)
template_path = os.path.join(parent_dir, "Templates", "Q_heat_and_ventilation_template.docx")
out_folder = os.path.join(current_dir, "reports")
pprint(short_context)
# render_docx(template_path=template_path, short_context=short_context, out_folder=out_folder, doc_name="base_data.docx")