"""
README
"""
# Importing random tools module
import random

# Import module permutations
from itertools import permutations

"""
GOOGLE SPREADSHEET FUNCTION
"""

"""
Splitter List
Recuirement: must be list with a value with delimiter
Example: andri.muhyidin
Result: ['andri','muhyidin']
"""
def gsheet_split(gsheet_entity_value,delimiter):
    result = []
    for i in gsheet_entity_value:
        result.append(i.split(delimiter))
    return result

"""
Filtering List with Len
Recuirement: A is normal list, B is nested list
Example: A=['andri','muhyidin'] B=[['andri'],['andri','muhyidin'],['andri','muhyidin','top']]
Result: ['andri','muhyidin']
"""
def gsheet_filter(entity_value,gsheet_split):
    result = []
    for item in gsheet_split:
        if len(item) == len(entity_value):
            result.append(item)
    return result

"""
Get Answer
"""
def gsheet_answer(entity_value,gsheet_split,gsheet_filter,gsheet_list_answer):
    for item in permutations(entity_value):
        if list(item) in gsheet_filter:
            index = gsheet_split.index(list(item))
            result = random.choice(gsheet_list_answer)[index]
            break
    return result

"""
All Step
1. Split the list entity value in google sheet
2. Filter if same len between param and split result
3. Permutation to get index for the respons
"""
def gsheet_all(entity_value,gsheet_entity_value,gsheet_list_answer):
    result_split = gsheet_split(gsheet_entity_value,'.')
    result_filter = gsheet_filter(entity_value,result_split)
    speech = gsheet_answer(entity_value,result_split,result_filter,gsheet_list_answer)
    return speech