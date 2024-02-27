import os
import inspect
import sys
import pandas as pd
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from GSOPCalculator.GSOPProcess.CreateGSOPData import CalculateGSOP
from GSOPCalculator.GSOPView.CalculateGSOPView import CalculateGSOPView
from EnergyCompare.Utility.PandasFunctions import load_input_data_frame
from SpExcelDB.SqlConnector import DB_TABLE,SqlConnector
from SpExcelDB.ExcelDBPath import ExcelDBPath

class GSOPControl:
	def __init__(self):
		# climat_df = pd.read_sql("select * from ClimatData",SqlConnector.conn_local_sql)
		climat_df = load_input_data_frame(ExcelDBPath.climate_data)
		self.gsop_view = CalculateGSOPView()
		self.gsop_model = CalculateGSOP(climat_df)
		self.gsop_view.all_regions = self.gsop_model.all_regions
		self.gsop_view.all_city = self.gsop_model.all_city
		self.gsop_view.create_view(self.gsop_model.df)
		self.gsop_model.selected_region = self.gsop_view.selected_region
		self.gsop_view.unique_city = self.gsop_model.unique_city
		self.gsop_model.selected_city = self.gsop_view.selected_city
  
	def calculate_gsop(self):
		return self.gsop_model.gsop
		
