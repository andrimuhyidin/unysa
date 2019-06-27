"""
README
"""
import random
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
def split_list_value(list_data,delimiter):
    result = []
    for i in list_data:
        result.append(i.split(delimiter))
    return result

"""
Filtering List with Len
Recuirement: A is normal list, B is nested list
Example: A=['andri','muhyidin'] B=[['andri'],['andri','muhyidin'],['andri','muhyidin','top']]
Result: ['andri','muhyidin']
"""
def filter_list_value(listA,listB):
    result = []
    for item in listB:
        if len(item) == len(listA):
            result.append(item)
    return result

"""
Get Answer
"""
def ans_list_value(listA,listB,listFilter,listAns):
    result = ''
    for item in permutations(listA):
        if list(item) in listFilter:
            index = listB.index(list(item))
            result = random.choice(listAns)[index]
            break
    return result

"""
All Step
"""
def gsheet_all(sheet_entity_value,delimiter,entity_value,sheet_answer):
    # Split the list entity value in google sheet
    result_split = split_list_value(sheet_entity_value,delimiter)
    # Filter if same len between param and split result
    result_filter = filter_list_value(entity_value,result_split)
    # Permutation to get index for the respons
    result_ans = ans_list_value(entity_value,result_split,result_filter,sheet_answer)
    return result_ans

"""
Store Data as List
"""
def convert_temp(tempData):
    storeData = []
    for i in tempData:
        for j in i:
            storeData.append(j)
    return storeData