#!/usr/bin/python

import csv
import os
from urlparse import urlparse

targetOutput = open("/Users/phisanshukkhi/Desktop/filtered.csv", "wb")
writer = csv.writer(targetOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
rows = csv.reader(open("/Users/phisanshukkhi/Desktop/items.csv","rb"))

count = 0
for row in rows:
    if len(row) != 0:
        url = row[0]
        path = urlparse(url).path
        ext = os.path.splitext(path)[1]

        if ext!=".jpg" and ext!=".jpeg" and ext!=".JPG" and ext!=".JPEG" and ext!=".pdf" and ext!=".doc" and ext!=".gif" and ext!=".swf" and ext!=".png" and ext!=".js":
            newrow = ['health.sanook.com', row[0]]
            writer.writerow(newrow)
            count += 1

targetOutput.close()
