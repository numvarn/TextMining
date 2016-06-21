#!/usr/bin/python

import csv
import os
from urlparse import urlparse

filterNetLoc = ["med.mahidol.ac.th"]

targetOutput = open("/Users/phisanshukkhi/Desktop/filtered.csv", "wb")
writer = csv.writer(targetOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
rows = csv.reader(open("/Users/phisanshukkhi/ResearchCode/TextMining/webcrawler/TextMining/spiders/items.csv","rb"))

netloclist = []
urllist = []
desclist = []
for row in rows:
    if row[0] in filterNetLoc and row[1] not in urllist:
        netloclist.append(row[0])
        urllist.append(row[1])
        desclist.append(row[2])

index = 0
for netloc in netloclist:
    url = urllist[index]
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]

    if ext!=".jpg" and ext!=".jpeg" and ext!=".JPG" and ext!=".JPEG" and ext!=".pdf" and ext!=".doc" and ext!=".gif" and ext!=".swf" and ext!=".png" and ext!=".js":
        newrow = []
        newrow.append(netloclist[index])
        newrow.append(urllist[index])
        newrow.append(desclist[index])
        writer.writerow(newrow)

    index += 1

targetOutput.close()
