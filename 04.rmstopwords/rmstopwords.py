#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
import sys
import csv

def readStopWords():
    stopwords = []
    rows = csv.reader(open("./stopwords.csv", "rb"))
    for row in rows:
        stopwords.append(row[0].decode('utf-8'))
    return stopwords

def removeStopWords(filepath, destination_dir, filename, stopwords):
    f = open(filepath+"/"+filename, 'r')
    ft = open(destination_dir+"/"+filename, 'w')
    lineword = []
    for line in iter(f):
        newline = ''
        string = line.decode('utf-8')
        words = string.split("|")
        index = 0
        for word in words:
            if word in stopwords or word == "":
                del words[index]
            index += 1

        newline = "|".join(words)+"\n"
        newline = newline.encode('utf-8')
        ft.write(newline)

    f.close()
    ft.close()

def main():
    stopwords = readStopWords()
    if len(sys.argv) != 1:
        filedir = sys.argv[1]

        upone_level = path.dirname(filedir.rstrip('/'))
        uptwo_level = path.dirname(upone_level.rstrip('/'))
        destination_dir = uptwo_level+"/stopwords"

        # Create directory for store result file
        if not path.exists(destination_dir):
            makedirs(destination_dir)

        # List all file from target directory
        onlyfiles = [f for f in listdir(filedir) if isfile(join(filedir, f))]

        for filename in onlyfiles:
            print "Processing file : ", filename
            removeStopWords(filedir, destination_dir, filename, stopwords)
    else:
        print "Please, Enter File Directory"

if __name__ == '__main__':
    main()

