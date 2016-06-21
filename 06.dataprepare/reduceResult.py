#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
import sys
import csv

def reduceResult(resultFile, symptomsID):
    print "Processing : ", resultFile
    rows = csv.reader(open(resultFile, "rb"))
    rowNumber = 0
    herblist = []
    for row in rows:
        if rowNumber > 0:
            value = 0
            for index in xrange(2, len(herblist)-1):
                value = int(row[index])
                herblist[index - 2] += value
        else:
            herblist = [0] * (len(row) - 3)
        rowNumber += 1

    # write new csv file
    destRootPath = path.dirname(resultFile.rstrip('/'))
    destRootPath = path.dirname(destRootPath.rstrip('/'))
    destRootPath = destRootPath+"/002.filtered"

    # Create directory for store result file
    if not path.exists(destRootPath):
        makedirs(destRootPath)

    destPath = destRootPath+"/"+symptomsID+"-filtered.csv"
    outfile = open(destPath, 'w')

    rows = csv.reader(open(resultFile, "rb"))
    rowCount = 0
    for row in rows:
        newrow = []
        newrow.append(row[0])

        for index in xrange(2, len(herblist)-1):
            if herblist[index - 2] >= (0.2 * rowNumber):
                newrow.append(row[index])

        # check total frequentcy in each row
        rowSumation = 0
        if rowCount > 0:
            for index in xrange(2, len(newrow)- 1):
                rowSumation += int(newrow[index])

        if rowSumation != 0 or rowCount == 0:
            newline = ",".join(newrow)+"\n"
            newline = newline.encode('utf-8')
            outfile.write(newline)

        rowCount += 1

    outfile.close()

def main():
    if len(sys.argv) == 2:
        rootPath = sys.argv[1]
        onlyfiles = [f for f in listdir(rootPath) if isfile(join(rootPath, f))]

        for resultFile in onlyfiles:
            symptomsID, ext = resultFile.split(".")
            if ext == "csv":
                reduceResult(rootPath+"/"+resultFile, symptomsID)
    else:
        print "Please, Enter File Directory"

if __name__ == '__main__':
    main()
