from pprint import pprint
import json

import pandas as pd


def save_json(json_text, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        json.dump(json_text, outfile, ensure_ascii=False)


df = pd.read_excel('renamed_table.xlsx', sheet_name='1', engine='openpyxl')
export_dict = df.to_dict('split')['data']
renamed_dict = {val[0]: val[1] for val in export_dict}
save_json(renamed_dict, '../StaticData/renamed_text.json')
