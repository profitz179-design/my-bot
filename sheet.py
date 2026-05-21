import gspread
from google.oauth2.service_account import Credentials
import os
import json

def get_sheet():
    scopes = ["https://spreadsheets.google.com/feeds",
              "https://www.googleapis.com/auth/drive"]
    
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    
    client = gspread.authorize(creds)
    return client.open_by_key(os.getenv("GOOGLE_SHEET_ID")).sheet1

def save_client(name, phone, chat_id):
    sheet = get_sheet()
    sheet.append_row([name, phone, str(chat_id)])
