import gspread, random
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

gc = gspread.authorize(credentials)

sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1gsMdyQqClto8t6rpLwxEirwghkMgalq_2rm2zUoK_bw/edit#gid=0")

worksheet = sh.worksheet("data_answer")

sheet_entity_type = worksheet.col_values(1)
sheet_entity_value = worksheet.col_values(2)
sheet_answer = [
    worksheet.col_values(3),
    worksheet.col_values(4),
    worksheet.col_values(5)
]