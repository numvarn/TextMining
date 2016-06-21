#!/usr/bin/python

import csv
rows = csv.reader(open("items.csv","rb"))
for row in rows:
    print row[1], row[2]
