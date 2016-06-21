#!/usr/bin/python
# -*- coding: utf-8 -*-

# Filter rule only show associaiton
# between symptoms and herb
# and convert code to thai langauage
# edited on 9 - 05 - 2016

import csv
import sys
from os import path
from os import listdir
from os import makedirs
from os.path import isfile, join

def readHerbList():
    herblist = []
    rows = csv.reader(open("./dictionary/herblist-21-04-16.csv", "rb"))
    for row in rows:
        herblist.append(row[1].strip())
    return herblist

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./dictionary/symptoms-21-04-16.csv", "rb"))
    for row in rows:
        symptoms.append(row[1].strip())
    return symptoms

def main(directory, filename, resultPath):
    print resultPath+"/"+filename
    herbCSV = readHerbList()
    sympCSV = readSymptoms()

    # Prepair CSV file to write result
    targetOutput = open(resultPath+"/"+filename, "w")
    writer = csv.writer(targetOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    newrow = ['No.', 'Premises', 'Conclusion', 'Support', 'Confidence', 'LaPlace', 'Gain', 'p-s', 'Lift', 'Conviction']
    writer.writerow(newrow)

    herbList = []
    sympList = []
    rows = csv.reader(open(directory+"/"+filename, "rb"))
    ruleCont = 0
    relationCount = 0
    rowCount = 0
    for row in rows:
        rowCount += 1
        if rowCount > 1:
            ruleCont += 1
            flagHerb = False
            flagSymp = False

            # analyze Premises
            premises_thai_list = []
            conclusion_thai_list = []

            premises = row[1].split(",")
            for item in premises:
                item = item.strip()
                if item[0] == 's':
                    flagSymp = True
                    if item not in sympList:
                        sympList.append(item)
                    # convert symptoms code to thai word
                    index = int(item[1:len(item)])
                    premises_thai_list.append(sympCSV[index].strip())
                elif item[0] == 'H':
                    flagHerb = True
                    if item not in herbList:
                        herbList.append(item)
                    # convert herb code to thai word
                    ext, hindex = item.split('-')
                    index = int(hindex)
                    premises_thai_list.append(herbCSV[index].strip())
            # analyze Conclusion
            conclusion = row[2].split(",")
            for item in conclusion:
                if item[0] == 's':
                    flagSymp = True
                    if item not in sympList:
                        sympList.append(item)
                    # convert symptoms code to thai word
                    index = int(item[1:len(item)])
                    conclusion_thai_list.append(sympCSV[index].strip())
                elif item[0] == 'H':
                    flagHerb = True
                    if item not in herbList:
                        herbList.append(item)
                    # convert herb code to thai word
                    ext, hindex = item.split('-')
                    index = int(hindex)
                    conclusion_thai_list.append(herbCSV[index].strip())

            if flagSymp == True and flagHerb == True:
                newrow = []
                row[1] = ','.join(premises_thai_list)
                row[2] = ','.join(conclusion_thai_list)
                newrow = row
                relationCount += 1
                writer.writerow(newrow)

    # Show result
    print "Founded Rules : ", ruleCont
    print "Founded Rules have relation between Symptoms and Herbs : ", relationCount, "\n"
    print "Founed Symptoms : ", len(sympList)
    for symp in sympList:
        index = int(symp[1:len(symp)])
        print sympCSV[index].strip(),'(', symp,') , ',

    print " "
    print "Founded Herbs : ", len(herbList)
    for herb in herbList:
        ext, hindex = herb.split('-')
        index = int(hindex)
        print herbCSV[index].strip(),'(', herb,') , ',
    print " "

    targetOutput.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        resultPath = '/Users/phisanshukkhi/Desktop/rulesThai'
        # Create directory for store result file
        if not path.exists(resultPath):
            makedirs(resultPath)

        onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
        for filename in onlyfiles:
            if filename != ".DS_Store":
                print filename
                main(directory, filename, resultPath)
    else:
        print "Please, Enter File Directory"

