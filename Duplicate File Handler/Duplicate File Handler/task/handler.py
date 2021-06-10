# write your code here
import collections
import os
import sys
import re
import hashlib
import sqlite3

args = sys.argv

if len(args) != 2:
    print('Directory is not specified')
    exit(-1)
path = args[1]

sorting_options = {'1': 'DESC', '2': 'ASC'}
file_format = input('Enter file format: ')
print('\nSize sorting options:\n\
1. Descending\n\
2. Ascending\n')
if file_format == '':
    file_format = '.*'
while True:
    option = input('Enter a sorting option: ')
    if option not in sorting_options:
        print('Wrong!\n')
    else:
        break

conn = sqlite3.connect('files.s3db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS files')
cur.execute('CREATE TABLE files(name TEXT, size INTEGER, hash VARCHAR(100))')
conn.commit()


def read_files_in_dir(path):
    for root, dic, files in os.walk(path, topdown=True):
        for name in files:
            if re.match('.*\.' + file_format + '$', str(name)):
                full_name = root + '\\' + name
                file_size = str(os.path.getsize(full_name))
                with open(full_name, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                cur.execute(f"INSERT INTO files(name, size, hash) VALUES('{full_name}', {file_size}, '{file_hash}')")
                conn.commit()


read_files_in_dir(path)
cur.execute(f'SELECT size, name FROM files ORDER BY size {sorting_options[option]}')
files_sorted_by_size = cur.fetchall()

if option == '1':
    current_size = sys.maxsize
else:
    current_size = -1
for file in files_sorted_by_size:
    file_size = file[0]
    file_name = file[1]
    if option == '1':
        if file_size < current_size:
            current_size = file_size
            print(f'\n{str(current_size)} bytes')
    else:
        if file_size > current_size:
            current_size = file_size
            print(f'\n{str(current_size)} bytes')
    print(file_name)
print()

while True:
    check_duplicates = input('Check for duplicates?\n')
    if check_duplicates == 'yes' or check_duplicates == 'no':
        print()
        break
    print('Wrong option\n')

if check_duplicates == 'yes':
    cur.execute(f'SELECT hash, name, size FROM files WHERE hash IN(SELECT hash FROM files GROUP BY hash HAVING COUNT(hash)>=2) ORDER BY 3 {sorting_options[option]}, 1 DESC')
    duplicate_files = cur.fetchall()
    current_size = -1
    current_hash = ""
    iterator = 1
    file_numbers = []
    for file in duplicate_files:
        hash_ = file[0]
        name = file[1]
        size = file[2]
        if size != current_size:
            print(f'\n{str(size)} bytes')
            current_size = size
        if hash_ != current_hash:
            print('Hash: ' + hash_)
            current_hash = hash_
        print(str(iterator) + '. ' + name)
        file_numbers.append(iterator)
        iterator += 1

    while True:
        delete = input('Delete files?\n')
        if delete == 'yes' or check_duplicates == 'no':
            print()
            break
        print('Wrong option\n')
    if delete == 'yes':
        while True:
            try:
                input_ = input('Enter file numbers to delete:\n')
                if input_ == '':
                    raise Exception
                files = [int(number) for number in input_.split()]
                temp = [x for x in file_numbers]
                for number in files:
                    if number in temp:
                        temp.remove(number)
                    else:
                        raise Exception
                break
            except Exception:
                print('\nWrong format\n')
                continue
        total_removed = 0
        for i in range(1, iterator):
            if i in files:
                os.remove(duplicate_files[i-1][1])
                total_removed += int(duplicate_files[i-1][2])
        print(f'Total freed up space: {total_removed} bytes')


cur.execute('DROP TABLE files')
conn.commit()
conn.close()
