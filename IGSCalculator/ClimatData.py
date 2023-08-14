import pandas as  pd
from DB.ExcelDBPath import ExcelDBPath


class CalculateGSOP:
    def __init__(self,climat_df:pd.DataFrame,city:str):
        self.gsop_model = CalculateGSOP(climate_df)
        self.gsop_model.selected_city = self.gsop_view.selected_city
climate_df =pd.read_excel(ExcelDBPath.climate_data)

gsop_data = CalculateGSOP(climate_df,)