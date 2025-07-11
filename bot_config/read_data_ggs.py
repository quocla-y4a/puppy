import gspread
import pandas as pd
import json
import os
import sys
import re
from airflow.models import Variable
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials


def read_data_ggsheet(spreadsheet_id: str, worksheet_name: str) -> pd.DataFrame:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(Variable.get("GOOGLE_SERVICE_ACCOUNT_JSON"))
    # creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes = scope)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.worksheet(worksheet_name)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df

spreadsheet_id = '1IGYFA6_78Ddp3idm1fZptWcQbI-8XNn8vgbA4gO256M'
worksheet_name = 'Sellin Comment Analysis'
df = read_data_ggsheet(spreadsheet_id, worksheet_name)

df.head()

df['posting_date'] = pd.to_datetime(df['posting_date'], format='%Y-%m')

