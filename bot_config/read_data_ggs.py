# import gspread
# import pandas as pd
# import json
# import os
# import sys
# import re
# from airflow.models import Variable
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from google.oauth2.service_account import Credentials
# from oauth2client.service_account import ServiceAccountCredentials
# from sqlalchemy import create_engine

import pygsheets
import pandas as pd
import os
import re
import sys


def read_sheet_data(spreadsheet_key, sheet_name, json_file):
    gc = pygsheets.authorize(service_file=json_file)
    sh = gc.open_by_key(spreadsheet_key)
    wks = sh.worksheet_by_title(sheet_name)

    records = wks.get_all_records(empty_value='', head=1, majdim='ROWS', numericise_data=False)
    df = pd.DataFrame(records)
    print(f"[INFO] Have read {len(df)} records from sheet '{sheet_name}'")
    return df

def update_sheet_data(spreadsheet_key, sheet_name, json_file, dataframe, clear_first=True, append=False):
    """
    Cập nhật dữ liệu vào Google Sheet.
    
    - Nếu `clear_first=True`: sẽ xoá sạch sheet trước khi ghi lại từ đầu.
    - Nếu `append=True`: sẽ append vào cuối sheet, không xoá dữ liệu cũ.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("`dataframe` must be a pandas DataFrame.")

    gc = pygsheets.authorize(service_file=json_file)
    sh = gc.open_by_key(spreadsheet_key)
    wks = sh.worksheet_by_title(sheet_name)

    dataframe.fillna('', inplace=True)

    if append:
        col1 = wks.get_col(1)
        next_row = len([i for i in col1 if i]) + 1
        wks.set_dataframe(dataframe, (next_row, 1), copy_head=False, nan='')
        print(f"[INFO] Append thành công {len(dataframe)} dòng vào dòng {next_row}")
    else:
        if clear_first:
            wks.clear()
            print(f"[INFO] Sheet '{sheet_name}' đã được xoá trước khi ghi mới")
        wks.set_dataframe(dataframe, (1, 1), copy_head=True, nan='')
        print(f"[INFO] Ghi đè thành công {len(dataframe)} dòng vào sheet '{sheet_name}'")

sheet_key = "1IGYFA6_78Ddp3idm1fZptWcQbI-8XNn8vgbA4gO256M"
sheet_name = "data"

json_cred = os.path.join(os.path.dirname(__file__), "credentials.json")
# json_cred = "credentials.json"

# Đọc dữ liệu
df = read_sheet_data(sheet_key, sheet_name, json_cred)

df['posting_date'] = pd.to_datetime(df['posting_date'], format='%m/%d/%Y')

print(df)


# Ghi đè dữ liệu mới
# df_new = pd.DataFrame([
#     {"name": "Alice", "age": 30},
#     {"name": "Bob", "age": 25},
# ])
# update_sheet_data(sheet_key, sheet_name, json_cred, df_new, clear_first=True)

# Hoặc thêm dòng mới vào cuối
# update_sheet_data(sheet_key, sheet_name, json_cred, df_new, append=True)
