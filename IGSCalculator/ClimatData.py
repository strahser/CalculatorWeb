import pandas as  pd
import os
import inspect
import sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from DB.ExcelDBPath import ExcelDBPath
from GSOPCalculator.GSOPProcess.CreateGSOPData import CalculateGSOP


class CalculateGSOPModel:
    def __init__(self,climat_df:pd.DataFrame,city:str):
        self.gsop_model = CalculateGSOP(climate_df)
        self.gsop_model.selected_city = city
        
climate_df =pd.read_excel(ExcelDBPath.climate_data)
gsop_data = CalculateGSOPModel(climate_df,"Москва")
out_dict = dict(gsop_str = gsop_data.gsop_model.gsop.gsop_str,
                t_in = gsop_data.gsop_model.building_property.t_in, 
                t_out = gsop_data.gsop_model.city_property.t_out,
                t_ot_per = gsop_data.gsop_model.city_property.t_ot_per,
                z_ot_per = gsop_data.gsop_model.city_property.z_ot_per,
                
)
print()