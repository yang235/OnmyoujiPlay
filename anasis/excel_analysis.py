import os
import pandas as pd


def read_excel():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '账户信息.xlsx')
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    return df.to_dict('records')