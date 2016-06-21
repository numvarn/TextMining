import csv

def main():
    # Read data from original source
    fileCSV = csv.reader(open("/Users/phisanshukkhi/Desktop/TF-IDF.csv", "rb"))
    herbStartPoint = 379
    herbEndPoint = herbStartPoint + 1006
    rowCount = 0

    # Prepair CSV file to write result
    targetOutput = open("/Users/phisanshukkhi/Desktop/TF-IDF-appy.csv", "wb")
    writer = csv.writer(targetOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    for row in fileCSV:
        print "processing row no.",rowCount
        maxWeight = 0
        maxIndex = herbStartPoint
        if rowCount > 0:
            for index in range(herbStartPoint, herbEndPoint):
                if row[index] != '':
                    value = 0.0
                    value = float(row[index])
                    if value != 0:
                        if value > maxWeight:
                            maxIndex = index
                            maxWeight = value
                        else:
                            row[index] = 0.0
                else:
                    row[index] = 0.0

            print rowCount,' : found max : ', maxIndex, ' weight : ', maxWeight

        writer.writerow(row)

        print ''
        rowCount += 1
        if rowCount > 20:
            break

if __name__ == '__main__':
    main()
