import gspread, random
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

gc = gspread.authorize(credentials)

sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1gsMdyQqClto8t6rpLwxEirwghkMgalq_2rm2zUoK_bw/edit#gid=0")

worksheet = sh.worksheet("ans_pendaftaran")

sheet_entity_type = worksheet.col_values(1)
sheet_entity_value = worksheet.col_values(2)
sheet_answer = [
    worksheet.col_values(3),
    worksheet.col_values(4),
    worksheet.col_values(5)
]
# Sample
entity_value = ['pengumuman','snmptnv2']

# Split value in sheet
sheet_entity_value_split = []
for i in sheet_entity_value:
    sheet_entity_value_split.append(i.split('.'))

# Create variable
sheet_entity_value_single = []
intersec = ''
# Check if item in value split
for sheet_entity_item in sheet_entity_value_split:
    # If all value on sheet same with entity value
    if all(element in sheet_entity_item for element in entity_value):
        # Take only value same with the criteria
        intersec = list(set(entity_value).intersection(sheet_entity_item))
        # index = sheet_entity_value_single.index(intersec)
# Test
print(intersec)
print(len(sheet_entity_value_split))
