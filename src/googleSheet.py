# Importing gspread module
import gspread

# Import creadential module
from oauth2client.service_account import ServiceAccountCredentials

# Create scope Google API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Importing creatential file "credentials.json" and scope API
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# New function name for authorized
gc = gspread.authorize(credentials)

# Link Gspread
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1gsMdyQqClto8t6rpLwxEirwghkMgalq_2rm2zUoK_bw/edit#gid=0")

# Worksheet name
worksheet = sh.worksheet("normal_respons")

# Create converter to lower text
def convert_low(list_data):
    result = []
    for element in list_data:
        result.append(element.lower())
    return result

# Take and convert value in google spreadsheet
gsheet_entity_intent = convert_low(worksheet.col_values(1))
gsheet_entity_type = convert_low(worksheet.col_values(2))
gsheet_entity_value = convert_low(worksheet.col_values(3))

# Get answer data
gsheet_list_answer = [
    worksheet.col_values(4),
    worksheet.col_values(5),
    worksheet.col_values(6),
    worksheet.col_values(7)
]

