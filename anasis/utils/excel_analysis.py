import os

import pandas as pd


def excel_analysis(file_name='../count_info.xlsx'):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, file_name)
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    return file_path, df

def read_excel():
    _, df = excel_analysis()
    return df.to_dict('records')


def count_info():
    rec_texts = read_excel()
    count_data = list({item['count'] for item in rec_texts})
    print(count_data)
    return count_data

def part_info(count_name):
    rec_texts = read_excel()
    return list({item['part'] for item in rec_texts if (item['count'] == count_name and item['mark'] == 0)})

def remark_info(count_name, new_parts):
    file_path, df = excel_analysis()
    parts = part_info(count_name)
    delete_part = [p for p in parts if p not in new_parts]
    mask = (df['count'] == count_name) & (df['part'].isin(delete_part))
    df.loc[mask, 'mark'] = 1
    df.to_excel(file_path, sheet_name='Sheet1', index=False)

def restart_mark():
    file_path, df = excel_analysis()
    df['mark'] = 0
    df.to_excel(file_path, sheet_name='Sheet1', index=False)

