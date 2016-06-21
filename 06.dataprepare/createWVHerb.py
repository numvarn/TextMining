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

def createVector(filepath, dirname, filename, herblist, symptoms, herbID):
    rowsize = len(symptoms) + 4
    row = [0]*rowsize
    fname, fext = filename.split(".")
    row[0] = "FID-"+fname
    row[1] = "HERBID-"+str(herbID)
    row[2] = dirname

    herbname = herblist[herbID]

    flagSymp = False
    flagHerb = False
    found_list = []

    src_file = open(filepath+"/"+filename, 'r')
    for line in iter(src_file):
        words = line.split("|")
        for word in words:
            if word == herbname:
                flagHerb = True
                break
        if flagHerb:
            break

    if flagHerb:
        for line in iter(src_file):
            words = line.split("|")
            index = 0
            for word in words:
                if word in symptoms:
                    flagSymp = True
                    index = symptoms.index(word)
                    if index not in found_list:
                        found_list.append(index)
                    row[index+3] += 1
        if flagSymp:
            found_list.sort()
            for index in xrange(0, len(found_list)):
                found_list[index] = str(found_list[index])
            row[len(row)-1] = ":".join(found_list)
            index = 0
            for item in row:
                row[index] = str(row[index])
                index += 1
            return row
        else:
            return []
    else:
        return []

def main(rootDir, dirname, herb_id, herblist, symptoms):
    filedir = rootDir+"/"+dirname+"/filtered2"
    herbID = int(herb_id)
    herb = herblist[herbID]

    print "Processing : ", dirname, " : ", herb

    # create path to write output file
    destination_dir = rootDir+"/WordVectorHerb"

    # Create directory for store result file
    if not path.exists(destination_dir):
        makedirs(destination_dir)

    dest_path = destination_dir+"/"+str(herbID)+"-"+herb+".csv"
    if isfile(dest_path):
        outfile = open(dest_path, 'a')
    else:
        outfile = open(dest_path, 'w')
        # create CSV Header
        header = ["filename", "herb", "netloc"]
        index = 0
        for symptom in symptoms:
            head = 's'+str(index)
            header.append(head)
            index += 1
        header.append("founded")

        newline = []
        newline = ",".join(header)+"\n"
        newline = newline.encode('utf-8')
        outfile.write(newline)

    # List all file from target directory
    onlyfiles = [f for f in listdir(filedir) if isfile(join(filedir, f))]
    for filename in onlyfiles:
        row = []
        row = createVector(filedir, dirname, filename, herblist, symptoms, herbID)
        if len(row) > 0:
            newline = []
            newline = ",".join(row)+"\n"
            outfile.write(newline)
    outfile.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Get root path from command line argument
        rootDir = sys.argv[1]

        # Read CSV
        herblist = readHerbList()
        symptoms = readSymptoms()

        herb_id = 0
        for herb in herblist:
            onlyDir = [ name for name in listdir(rootDir) if path.isdir(path.join(rootDir, name)) ]
            for dirname in onlyDir:
                if dirname != "WordVectorHerb" and dirname != "WordVectorHerbSymps":
                    main(rootDir, dirname, herb_id, herblist, symptoms)
            herb_id += 1
    else:
        print "Please, Enter File Directory"
