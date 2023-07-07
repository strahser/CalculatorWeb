
import os
import inspect
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)

class ExcelDBPath:
	"""
	сп 50, климатология, приказ 399
	сп 50
	http://sniprf.ru/sp50-13330-2012
	приказ 399
	https://normativ.kontur.ru/document?moduleId=1&documentId=278092
	"""
	sp_50_table_14 = os.path.abspath(os.path.join(current_dir,"ExcelDB", "sp_50_table_14.xlsx"))
	order_399_table1 = os.path.abspath(os.path.join(current_dir,"ExcelDB", "order_399_table1.xlsx"))
	climate_data = os.path.abspath(os.path.join(current_dir, "ExcelDB", "ClimateData.xlsx"))
