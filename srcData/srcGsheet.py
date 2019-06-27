import gspread, random
from oauth2client.service_account import ServiceAccountCredentials
from itertools import permutations

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

gc = gspread.authorize(credentials)

sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1gsMdyQqClto8t6rpLwxEirwghkMgalq_2rm2zUoK_bw/edit#gid=0")

worksheet = sh.worksheet("ans_pendaftaran")

sheet_entity_intent = worksheet.col_values(1)
sheet_entity_type = worksheet.col_values(2)
sheet_entity_value = worksheet.col_values(3)
sheet_answer = [
    worksheet.col_values(4),
    worksheet.col_values(5),
    worksheet.col_values(6),
    worksheet.col_values(7)
]

# Split value in sheet
sheet_entity_value_split = []
for i in sheet_entity_value:
    sheet_entity_value_split.append(i.split('.'))

# entity_value = ['SNMPTNV2','Pengumuman']
# sheet_value_filter = []
# for elemen in sheet_entity_value_split:
#     if len(elemen) == len(entity_value):
#         sheet_value_filter.append(elemen)

# # List permutation
# entity_value_permutation = permutations(entity_value)

# # Find same data
# for elemen in entity_value_permutation:
#     if list(elemen) in sheet_value_filter:
#         index = sheet_entity_value_split.index(list(elemen))
#         break

# print(f"yes {index} {list(elemen)} in {sheet_value_filter}")