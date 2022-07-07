#!/usr/bin/python3

import sys
import csv
import string
import random
import os
import time



def main():
    # command line checking
    if (len(sys.argv) != 3):
        print("Usage: ./fuzzer binary binaryinput.txt")
        sys.exit()


    binary = sys.argv[1]
    sampleInput = sys.argv[2]
    
    # TODO: check only run checking for 3mins - loop to call functions
    # for i in run(180):
    endTime = time.time() + 180
    while time.time() < endTime:

        manipulateCSVheader(sampleInput)
        os.system("cat modifiedHeader.csv | bin/./csv1")
        os.system("rm modifiedHeader.csv")
        modifiedData(sampleInput)
        os.system("cat modifiedHeader.csv | bin/./csv1")
        os.system("rm modifiedHeader.csv")

# generates a random ascii charatcers letters
def randomAsciiGen():
    return random.choice(string.ascii_letters)

def randomAsciiFromItem(item):
    choiceSelection = []
    for i in item:
       choiceSelection.append(i)
    return random.choice(choiceSelection)

# return a modified version of the header in sampleInput
def manipulateCSVheader(sampleInput):
    modifiedHeader = []
    sameData = []
    with open(sys.argv[2], mode='r') as sampleInput:
        for i,row in enumerate(csv.reader(sampleInput,delimiter=',')):

            # changing the ascii characters of the header
            for item in row:
                # only manipulate the header
                if i == 0:
                    charToReplace = randomAsciiFromItem(item)
                    if ( charToReplace in item):
                        item = item.replace(charToReplace,randomAsciiGen())
                        
                        modifiedHeader.append(item)
            if (i != 0):
                sameData.append(row)
    # write header to new file to run to program
    with open('modifiedHeader.csv',mode='w') as modifiedFile:
        writer = csv.writer(modifiedFile)
        writer.writerow(modifiedHeader)
        for i in sameData:
            writer.writerow(i)
    

    # TODO: sending in a null header

# send
selection = ["%s","\n","%n","A" * 999]
def modifiedData(sampleInput):
    modifiedData = []
    with open(sys.argv[2], mode='r') as sampleInput:
        for i,row in enumerate(csv.reader(sampleInput,delimiter=',')):
            # changing the ascii characters of the input
            newRow = []
            for item in row:
                # keep the header the same
                if i != 0:
                    item += randomAsciiFromItem(selection)
                    newRow.append(item)

            if (i == 0):
                modifiedData.append(row) 
            else:
                modifiedData.append(newRow)
    # write header to new file to run to program
    with open('modifiedHeader.csv',mode='w') as modifiedFile:
        writer = csv.writer(modifiedFile)
        for i in modifiedData:
            writer.writerow(i)


# TODO: send a modified delimiter ("\n,""(empty string),random char,%s")  
def modifiedDelimiter(sampleInput):
    pass

if __name__ == "__main__":
    main()

