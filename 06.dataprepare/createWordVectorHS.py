#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
import sys
import csv

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

def main(rootDir, dirname, herblist, symptoms):
    filedir = rootDir+"/"+dirname+"/filtered3"

    print "\nProcessing : ", filedir

    # create path to write output file
    destination_dir = rootDir+"/WordVectorHerbSymps"

    # Create directory for store result file
    if not path.exists(destination_dir):
        makedirs(destination_dir)

    dest_path = destination_dir+"/wordsVectorHS.csv"
    if isfile(dest_path):
        outfile = open(dest_path, 'a')
    else:
        outfile = open(dest_path, 'w')
        # create CSV Header
        header = ["filename", "dirname"]
        index = 0
        for symp in symptoms:
            head = 's'+str(index)
            header.append(head)
            index += 1

        index = 0
        for herb in herblist:
            head = 'h'+str(index)
            header.append(head)
            index += 1

        header.append('Found H')
        header.append('Found S')

        newline = []
        newline = ",".join(header)+"\n"
        newline = newline.encode('utf-8')
        outfile.write(newline)

    # Calculate row size
    row_size = len(symptoms) + len(herblist) + 2

    # Count keyword in each file
    onlyfiles = [f for f in listdir(filedir) if isfile(join(filedir, f))]
    for filename in onlyfiles:
        found_s_list = []
        found_h_list = []
        print "processing file : ", filename, " in ", dirname
        fname, fext = filename.split(".")
        row = [0] * row_size
        row[0] = "FID-"+fname
        row[1] = dirname

        # Open and Read file
        src_file = open(filedir+"/"+filename, 'r')
        for line in iter(src_file):
            words = line.split("|")
            for word in words:
                foundedH = ''
                foundedS = ''
                if word in symptoms:
                    row_index = symptoms.index(word) + 2
                    foundedS = symptoms.index(word)
                    row[row_index] += 1
                elif word in herblist:
                    row_index = herblist.index(word) + len(symptoms) + 2
                    foundedH = herblist.index(word)
                    row[row_index] += 1

                if foundedS != '' and foundedS not in found_s_list:
                    found_s_list.append(foundedS)
                if foundedH != '' and foundedH not in found_h_list:
                    found_h_list.append(foundedH)

        if len(found_h_list) != 0:
            found_h_list.sort()
            found_s_list.sort()

            for index in xrange(0,len(found_h_list)):
                found_h_list[index] = str(found_h_list[index])
            for index in xrange(0,len(found_s_list)):
                found_s_list[index] = str(found_s_list[index])

            row.append(':'.join(found_h_list))
            row.append(':'.join(found_s_list))

            # Convert Items to string
            row_str = []
            for item in row:
                row_str.append(str(item))

            # Write row in CSV file
            newline = ",".join(row_str)+"\n"
            newline = newline.encode('utf-8')
            outfile.write(newline)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Get root path from command line argument
        rootDir = sys.argv[1]

        # Read CSV
        herblist = readHerbList()
        symptoms = readSymptoms()

        onlyDir = [ name for name in listdir(rootDir) if path.isdir(path.join(rootDir, name)) ]
        dir_count = 0
        for dirname in onlyDir:
            if dirname != "WordVectorHerbSymps":
                main(rootDir, dirname, herblist, symptoms)
                dir_count += 1
                # if dir_count > 1:
                #     break
    else:
        print "Please, Enter File Directory"
