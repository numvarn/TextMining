#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
import sys
import csv
import numpy

def readHerbList():
    herblist = []
    rows = csv.reader(open("./herblist.csv", "rb"))
    for row in rows:
        herblist.append(row[1].strip())
    return herblist

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./symptoms.csv", "rb"))
    for row in rows:
        symptoms.append(row[1].strip())
    return symptoms

def main():
    if len(sys.argv) == 2:
        herbName = readHerbList()
        symptoms = readSymptoms()
        herbs = numpy.zeros((len(herbName), len(symptoms)))

        rootPath = sys.argv[1]
        onlyfiles = [f for f in listdir(rootPath) if isfile(join(rootPath, f))]

        breakCount = 0
        for resultFile in onlyfiles:
            print "Processing : ", resultFile
            symptomsID, ext = resultFile.split(".")
            if ext == "csv" and symptomsID != "counted":
                symptomsID = int(symptomsID)
                rows = csv.reader(open(rootPath+"/"+resultFile, "rb"))
                rowNumber = 0
                for row in rows:
                    if rowNumber > 0:
                        for h_index in xrange(2, len(herbName)):
                            herbs[h_index-2][symptomsID] += int(row[h_index])
                    rowNumber += 1

            breakCount += 1
            # if breakCount >= 5:
            #     break

        # Write result to CSV
        destPath = rootPath+"/counted.csv"
        outfile = open(destPath, 'w')

        h_index = 0
        for h in herbName:
            newrow = []
            h_sum = 0
            if h_index == 0:
                newrow.append("HERP")
            else:
                newrow.append("h"+str(h_index)+"-"+herbName[h_index])

            s_index = 0
            for s in symptoms:
                if h_index == 0:
                    newrow.append("SYMP"+str(s_index)+"-"+symptoms[s_index])
                else:
                    h_sum += herbs[h_index][s_index]
                    newrow.append(str(int(herbs[h_index][s_index])))
                s_index += 1

            if h_index == 0:
                newrow.append("Total")
            else:
                newrow.append(str(int(h_sum)))

            newline = ",".join(newrow)+"\n"
            # newline = newline.encode('utf-8')
            outfile.write(newline)

            h_index += 1
    else:
        print "Please, Enter File Directory"

if __name__ == '__main__':
    main()
