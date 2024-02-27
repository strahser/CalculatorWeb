
import os
import inspect
import sys
import sqlite3
import pandas as pd
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)

DB_NAME = os.path.join(current_dir,"export_excel.db")
DB_TABLE = dict(ClimatData="ClimatData.xlsx",q_0="q_0.xlsx")

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class SqlConnector(object):
    __metaclass__ = Singleton
    memory_connection_path = "file::memory:?cache=shared"
    conn_sql: sqlite3.Connection = sqlite3.connect(memory_connection_path, uri=True, check_same_thread=False)
    conn_local_sql: sqlite3.Connection = sqlite3.connect( DB_NAME, check_same_thread=False)

def create_tables_from_excel(excel_tables:dict[str,str]):
    for db_new_name,excel_file_name in excel_tables.items():
        path =os.path.join(current_dir, "ExcelDB", excel_file_name)
        table = pd.read_excel(path)
        table.to_sql(name=db_new_name,con=SqlConnector.conn_local_sql,if_exists="replace")
        
if __name__=="__main__":
    create_tables_from_excel(DB_TABLE)