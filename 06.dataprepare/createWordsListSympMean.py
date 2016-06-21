#!/usr/bin/python
# -*- coding: utf-8 -*-

# Calculate TF-IDF Weight
# Create word list with IDF weight
# Using mean value to keywords filtering

import sys
import csv
import math
from os import listdir
from os.path import isfile, join
from os import path
from os import makedirs

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./dictionary/symptoms-21-04-16.csv", "rb"))
    for row in rows:
        symptoms.append(row[1].strip())
    return symptoms

def main(directory, filename, resultPath):
    # Read CSV
    symptoms = readSymptoms()

    wordsSymp = [0] * (len(symptoms) + 1)

    wordsSymp[0] = ["Symptoms", "Code", "Total Occurences", "Document Occurences", "Total Occurences(%)", "Document Occurences(%)", "IDF", "IDF filtered"]

    index = 0
    for row in wordsSymp:
        if index > 0:
            wordsSymp[index] = [0, 0, 0, 0, 0, 0, 0, 0]
        index += 1

    index = 1
    for symp in symptoms:
        wordsSymp[index][0] = symp
        wordsSymp[index][1] = 's'+str(index-1)
        index += 1

    row_count = 1
    print directory+"/"+filename
    rows = csv.reader(open(directory+"/"+filename))

    totalDocument = 0
    for row in rows:
        if row_count > 1:
            totalDocument += 1
            column_count = 0
            for item in row:
                if column_count > 2 and column_count <= len(symptoms) + 1:
                    sindex = column_count - 3
                    wordsSymp[sindex+1][2] += + int(row[column_count])
                    if int(row[column_count]) != 0:
                        wordsSymp[sindex+1][3] += 1
                column_count += 1
        row_count += 1

        # print "Processing row #",row_count-1

    feq_total_sym = 0
    row_count = 0
    for row in wordsSymp:
        if row_count > 0:
            feq_total_sym += row[2]
        row_count += 1

    row_count = 0
    total_idf_weight = 0
    member_notZero_count = 0
    for row in wordsSymp:
        if row_count > 0:
            if feq_total_sym != 0:
                wordsSymp[row_count][4] = (float(row[2]) / float(feq_total_sym)) * 100
            if totalDocument != 0:
                wordsSymp[row_count][5] = (float(row[3]) / float(totalDocument)) * 100
            if wordsSymp[row_count][2] != 0:
                wordsSymp[row_count][6] = math.log10(totalDocument / wordsSymp[row_count][3])
                total_idf_weight += wordsSymp[row_count][6]
                member_notZero_count += 1

        row_count += 1

    # Calculate mean of IDF weight
    mean_idf = 0
    if member_notZero_count != 0:
        mean_idf = total_idf_weight / member_notZero_count
        mean_idf = "{0:.2f}".format(mean_idf)

    print "Mean IDF : ", mean_idf

    row_count = 0
    for row in wordsSymp:
        if row_count > 0:
            if float(wordsSymp[row_count][6]) >= float(mean_idf):
                wordsSymp[row_count][7] = wordsSymp[row_count][6]
            else:
                wordsSymp[row_count][7] = 0
        row_count += 1

    # Write result to CSV
    destination_dir = resultPath+"/wordList"
    if not path.exists(destination_dir):
        makedirs(destination_dir)

    destPath = destination_dir+"/"+filename
    with open(destPath, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(wordsSymp)

    # Calculate TF-IDF for each term
    destination_dir = resultPath+"/vectorTFIDF-keywordsFiltered"
    if not path.exists(destination_dir):
        makedirs(destination_dir)

    destFile = destination_dir+"/"+filename
    outfile = open(destFile, 'w')

    rows = csv.reader(open(directory+"/"+filename))
    row_count = 0

    for row in rows:
        new_row = []
        column_index = 0
        if row_count > 0:
            for term_feq in row:
                wordList_index = column_index - 2
                if 2 < column_index < len(symptoms) + 3:
                    if int(term_feq) != 0:
                        # term_idf = wordsSymp[wordList_index][6]

                        #-- Filtering keywords --#
                        term_idf = wordsSymp[wordList_index][7]
                        weight = float(term_feq) * float(term_idf)
                        weight = "{0:.2f}".format(weight)
                        new_row.append(str(weight))
                    else:
                        new_row.append(term_feq)
                else:
                    new_row.append(term_feq)
                column_index += 1

            newline = ",".join(new_row)+"\n"
            newline = newline.encode('utf-8')
            outfile.write(newline)
        else:
            for header in row: new_row.append(header)
            newline = ",".join(new_row)+"\n"
            newline = newline.encode('utf-8')
            outfile.write(newline)

        row_count += 1

    outfile.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        resultPath = '/Users/phisan/Desktop'

        onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
        for filename in onlyfiles:
            if filename != ".DS_Store":
                main(directory, filename, resultPath)
    else:
        print "Please, Enter File Directory"



