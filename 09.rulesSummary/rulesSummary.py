#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from os import listdir
from os import path
from os.path import isfile, join

def totalFileSummarize(file_name, file_path):
    name, ext = file_name.split('.')
    number, herb_name = name.split('-')
    print number," : ", herb_name

    # outfile
    outfile = open('./summary.csv', 'a')
    row_count = 0
    file_count = 0
    with open(file_path) as f:
        for row in f:
            if row_count > 0:
                file_count += 1
            row_count += 1

    summary = [number, herb_name, str(file_count)]
    newline = ",".join(summary)+"\n"
    outfile.write(newline)
    outfile.close()

def main():
    path = '/Users/phisan/Desktop/Data/010.result-9-05-2016/vertorTF'

    # init outfile
    outfile = open('./summary.csv', 'a')
    header = ['No.', 'Herb Name', 'Number of File']
    newline = ",".join(header)+"\n"
    outfile.write(newline)
    outfile.close()

    # List all file from target directory
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for filename in onlyfiles:
        #find number of file in earch category
        file_path = path+'/'+filename
        if filename != '.DS_Store':
            totalFileSummarize(filename, file_path)

if __name__ == '__main__':
    main()
