# write your code here
import collections
import os
import sys
import re

args = sys.argv

if len(args) != 2:
    print('Directory is not specified')
    exit(-1)
sorting_options = {'1': False, '2': True}
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
for root, dirs, files in os.walk(args[1], topdown=sorting_options[option]):
    for name in files:
        if re.match('.*\.' + file_format + '$', str(name)):
            result_files[root + '\\' + name] = str(os.path.getsize(root + '\\' + name))

flipped = {}

for key, value in result_files.items():
    if value not in flipped:
        flipped[value] = [key]
    else:
        flipped[value].append(key)

flipped = collections.OrderedDict(sorted(flipped.items()))

for item in flipped:
    if len(flipped[item]) >= 2:
        print(item + ' bytes')
        for file in flipped[item]:
            print(file)
        print()
