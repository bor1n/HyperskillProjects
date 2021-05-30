# write your code here
import collections
import os
import sys
import re

args = sys.argv

if len(args) != 2:
    print('Directory is not specified')
    exit(-1)
sorting_options = {'1': True, '2': False}
file_format = input('Enter file format: ')
print('\nSize sorting options:\n\
1. Descending\n\
2. Ascending\n')
if file_format == '':
    file_format = '.*'
while True:
    option = input('Enter a sorting option: ')
    print()
    if option not in sorting_options:
        print('Wrong!\n')
    else:
        break
result_files = {}
for root, dic, files in os.walk(args[1]):
    for name in files:
        if re.match('.*\.' + file_format + '$', str(name)):
            full_name = root + '\\' + name
            file_size = os.path.getsize(full_name)
            if file_size in result_files:
                result_files[file_size] += '\n' + full_name
            else:
                result_files[file_size] = full_name

sorted_keys = sorted(result_files.keys(), reverse=sorting_options[option])
for item in sorted_keys:
    if len(result_files[item]) >= 2:
        print(str(item) + ' bytes')
        print(result_files[item] + '\n')
