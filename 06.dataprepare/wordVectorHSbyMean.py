#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import math

# Create WordList and Words Vector of Herb and Symptoms
# And filter Symptom by using TFIDF mean in each document

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./dictionary/symptoms-21-04-16.csv", "rb"))
    for row in rows:
        symptoms.append(row[1].strip())
    return symptoms

def main():
    symptoms = readSymptoms()

    # Create new words vector and Write result to CSV
    rootPath = "/Users/phisan/Desktop"
    destFile = rootPath+"/wordsVectorHS-TFIDF-Symp-filter-mean.csv"
    outfile = open(destFile, 'w')

    wordVectorTFIDF = csv.reader(open("/Users/phisan/Desktop/007.WordVectorHerbSymps/04-wordsVectorHS-TFIDF-Symp.csv", "rb"))
    row_count = 1
    for row in wordVectorTFIDF:
        tfidf_list = []
        if row_count > 1:
            new_row = []
            for col_index in xrange(2, len(symptoms)+2):
                tfidf = float(row[col_index])
                if tfidf > 0:
                    tfidf_list.append(tfidf)
            total = 0
            for value in tfidf_list: total += value

            mean = 0.0
            if len(tfidf_list) > 0:
                mean = total / len(tfidf_list)

            less_list = []
            for col_index in xrange(2, len(symptoms)+2):
                tfidf = float(row[col_index])
                if 0 < tfidf < mean:
                    row[col_index] = str(0)
                    less_list.append(col_index - 2)

            print row[0] ," : mean", mean, " : ", less_list

            newline = ",".join(row)+"\n"
            newline = newline.encode('utf-8')
            outfile.write(newline)
        else:
            newline = ",".join(row)+"\n"
            newline = newline.encode('utf-8')
            outfile.write(newline)


        row_count += 1

if __name__ == '__main__':
    main()
