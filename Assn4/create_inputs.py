#!/usr/bin/env python3
PATH = "./logs/input/input"

def generate_files(num):
    n = num
    while num:
        with open(PATH + str(num) + '.txt', 'w', encoding='utf-8') as fd: 
            fd.write(msg)
        num -= 1
    print(f'Successfully wrote into {n} files')

filecount = int(input('Enter Number of Files: '))
msg = input('Enter text: ')
if len(msg) in (15, 30, 50): 
    generate_files(filecount)
else:
    res = input("Not Desired Length. Still opt to Write? (y/N): ")
    if res in ('y', 'Y'): 
        generate_files(filecount)