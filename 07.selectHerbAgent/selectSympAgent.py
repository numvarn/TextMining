import csv

def main():
    # Read data from original source
    fileCSV = csv.reader(open("/Users/phisanshukkhi/Desktop/TF-IDF.csv", "rb"))
    sympStartPoint = 0
    sympEndPoint = 379
    rowCount = 0

    # Prepair CSV file to write result
    targetOutput = open("/Users/phisanshukkhi/Desktop/TF-IDF-appy.csv", "wb")
    writer = csv.writer(targetOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    for row in fileCSV:
        print "processing row no.",rowCount
        if rowCount > 0:
            valueArr = []
            for index in range(sympStartPoint, sympEndPoint):
                if row[index] != '':
                    value = 0.0
                    value = float(row[index])
                    if value != 0:
                        print rowCount," : s",index, " : ",value
                        valueArr.append(value)
                else:
                    row[index] = 0.0

            # Get average value
            size = len(valueArr)
            summation = 0
            averageValue = 0
            for value in valueArr:
                summation += value
            averageValue = summation / size
            print "Average Value is : ", averageValue
            print "\nFilter by Mean\n"
            for index in range(sympStartPoint, sympEndPoint):
                value = 0.0
                value = float(row[index])
                if value != 0:
                    if value < averageValue:
                        row[index] = 0.0
                    else:
                        print rowCount," : s",index, " : ",value

        writer.writerow(row)

        print ''
        rowCount += 1
        # if rowCount > 10:
        #     break

if __name__ == '__main__':
    main()
