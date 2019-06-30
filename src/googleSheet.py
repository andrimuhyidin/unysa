import gspread, random
from oauth2client.service_account import ServiceAccountCredentials
import random

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1gsMdyQqClto8t6rpLwxEirwghkMgalq_2rm2zUoK_bw/edit#gid=0")

worksheet = sh.worksheet("normal_respons")

def convert_low(list_data):
    result = []
    for element in list_data:
        result.append(element.lower())
    return result

gsheet_entity_intent = convert_low(worksheet.col_values(1))
gsheet_entity_type = convert_low(worksheet.col_values(2))
gsheet_entity_value = convert_low(worksheet.col_values(3))

gsheet_list_answer = [
    worksheet.col_values(4),
    worksheet.col_values(5),
    worksheet.col_values(6),
    worksheet.col_values(7)
]

