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
Permutation
Get Index
"""
def ans_list_value(listA,listB,listFilter,listAns):
    result = ''
    for item in permutations(listA):
        if list(item) in listFilter:
            index = listB.index(list(item))
            result = random.choice(listAns)[index]
            break
    return result
