#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import urlopen
from os import listdir
from os.path import isfile, join
import os
import sys

def getWeb(filename, directory):
    print 'processing file : ', filename
    # process from local html file
    file_path = directory+'/original/'+filename

    # get filename
    file_name, file_ext = filename.split(".")

    # check file is exist before process
    if os.path.isfile(file_path):
        html = urlopen(file_path).read()

        soup = BeautifulSoup(html, 'html.parser')

        # for none utf-8 web page
        if soup.original_encoding != 'utf-8':
            try :
                decoded_html = html.decode('tis-620')
                soup = BeautifulSoup(decoded_html, 'html.parser')
            except :
                print "Dectect error ", filename
                pass

        # remove all Hyperlink in web page
        to_extract = soup.findAll('a')
        for item in to_extract:
            item.extract()

        # remove javascript
        to_extract = soup.findAll('script')
        for item in to_extract:
            item.extract()

        # remove inner CSS
        to_extract = soup.findAll('style')
        for item in to_extract:
            item.extract()

        # check current document is HTML or FEED
        # text = soup.body.get_text()
        text = soup.get_text()
        text = u''.join(text).encode('utf-8').strip()

        # process for file name from url
        target = directory+'/processed2/'
        if not os.path.exists(target):
            os.makedirs(target)
        filename = target+file_name+'.txt'

        # write result to file
        writeToFile(text, filename, directory)
    else:
        print "file ID "+filename+" is not exist."

def writeToFile(str, filename, directory):
    # write data in tmp file
    tmpfile = directory+"/tmp.txt"
    file = open(tmpfile, 'w')
    file.write(str)
    file.close()

    removeEmptyLine(filename, tmpfile)

    # remove tmp file
    if os.path.exists(tmpfile):
        os.remove(tmpfile)

def removeEmptyLine(filename, tmpfile):
    newcontent = []
    file1 = open(tmpfile, 'r')

    for line in file1:
        if not line.strip():
            continue
        else:
            newcontent.append(line)

    # write data in target file
    filecontent = "".join(newcontent)
    file2 = open(filename, 'w')
    file2.write(filecontent)
    file2.close()

# Start program
def main(filedir):
    filedir_tofile = filedir+"/original"
    onlyfiles = [f for f in listdir(filedir_tofile) if isfile(join(filedir_tofile, f))]
    for filename in onlyfiles:
            getWeb(filename, filedir)

# Main Program
# Get Network Location from command line argument
if __name__ == '__main__':
    if len(sys.argv) != 1:
        main(sys.argv[1])
    else:
        print "Please, Enter Network Location"

