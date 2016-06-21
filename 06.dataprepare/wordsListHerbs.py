#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import math

def readHerbList():
    herblist = []
    rows = csv.reader(open("./herblist-17-04-16.csv", "rb"))
    for row in rows:
        herblist.append(row[1].strip())
    return herblist

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./symptoms-17-04-16.csv", "rb"))
    for row in rows:
        symptoms.append(row[1].strip())
    return symptoms

def main():
    # Read CSV
    herblist = readHerbList()
    symptoms = readSymptoms()

    wordHerb = [0] * (len(herblist) + 1)

    wordHerb[0] = ["Herbs", "Code", "Total Occurences", "Document Occurences", "TF-IDF"]

    index = 0
    for row in wordHerb:
        if index > 0:
            wordHerb[index] = [0, 0, 0, 0, 0]
        index += 1

    index = 1
    for herb in herblist:
        wordHerb[index][0] = herb
        wordHerb[index][1] = 'h'+str(index-1)
        index += 1

    filename = '230-มะเร็ง.csv'
    filename_dest = '230-มะเร็ง.csv'
    row_size = len(symptoms) + len(herblist) + 1
    row_count = 1
    rows = csv.reader(open("/Users/phisan/Desktop/word-vector-symps/"+filename))
    for row in rows:
        if row_count > 1:
            column_count = 0
            for item in row:
                if column_count > 1 and column_count < len(herblist):
                    wordHerb[column_count][2] += int(row[column_count])
                    if int(row[column_count]) != 0:
                        wordHerb[column_count][3] += 1
                column_count += 1
        row_count += 1

        print "Processing row - ",row_count, "File #",row[0]

    total_document = row_count - 2

    row_count = 0
    for row in wordHerb:
        if row_count >= 1 and float(row[3]) > 0:
            row[4] = math.log10(total_document / row[3])
        row_count += 1
        print row[0], " \t", row[1], " \t", row[2], " \t", row[3], " \t", row[4], " \t"

    # Write result to CSV
    destPath = "/Users/phisan/Desktop/wordListHerbs/"+filename_dest
    with open(destPath, "wb") as fh:
        writer_h = csv.writer(fh)
        writer_h.writerows(wordHerb)

    print "Total Documents : ", total_document

if __name__ == '__main__':
    main()



