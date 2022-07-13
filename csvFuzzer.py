#!/usr/bin/python3

import sys
import csv
import string
import random
import os
import time
from pwn import *

sampleInput = "bin/csv1.txt"

def main():

    io = process("bin/csv1")
    # loop through the list!
    sendDataToTwls(modifiedData(sampleInput),io)
    sendDataToTwls(addLines(sampleInput),io)
    io.interactive()

    # TODO: check only run checking for 3mins - loop to call functions
    # for i in run(180):
    # endTime = time.time() + 180
    # while time.time() < endTime:


def sendDataToTwls(inputList,process):
    for line in inputList:
        print(line.encode())
        process.sendline(line.encode())


# generates a random ascii character from ascii_letters constant(combination of both upper and lower case)
def randomAsciiGen():
    return random.choice(string.ascii_letters)

# choose a random ascii from a list of choices
def randomAsciiFromItem(selection):
    return random.choice(selection)

# convert the csv file to a 2d list with each index into array being a line
# for exam a csv file containing:
# -----------------------------
# header,must,stay,intact
#a,b,c,S
#e,f,g,ecr
#i,j,k,et
# --------------------------------
# will output to [[header,must,stay,intact],[a,b,c,S],[e,f,g,ecr],[i,j,k,et]]
def convertCsvToList(csvFile):
    outputList = []
    with open(csvFile, mode='r') as f:
        for row in csv.reader(f,delimiter=','):
            outputList.append(row)
    return outputList

# return a modified version of the header in sampleInput
def manipulateCSVheader(sampleInput):
    modifiedHeader = []
    sameData = []
    with open(sampleInput, mode='r') as sampleInputFile:
        for i,row in enumerate(csv.reader(sampleInputFile,delimiter=',')):
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
    return convert2DList(modifiedData,',')

# send
selection = ["%s","%n","A"*99, "%n"]
def modifiedData(sampleInput):
    modifiedData = []
    with open(sampleInput, mode='r') as sampleInputFile:
        for i,row in enumerate(csv.reader(sampleInputFile)):
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

    return convert2DList(modifiedData,',')

def convert2DList(list,delimiter):
    retList = []
    for i,row in enumerate(list):
        newLine = ""
        for j,word in enumerate(row):
            if (j != 0):
                newLine += delimiter + word
            elif (j == 0):
                newLine = word
        retList.append(newLine)
    return retList


# send a modified delimiter ("\n,""(empty string),random char,%s")  
def modifiedDelimiter(sampleInput):
    modifiedDelimiter = ["\n","","%","%n","%s","%d",randomAsciiGen()]
    return convert2DList(convertCsvToList(sampleInput), random.choice(modifiedDelimiter))

def addLines(sampleInput):
    data = convertCsvToList(sampleInput)
    row = ["%n","%d","%s","%p"]
    # choose the number of times to loop over and add row of data
    selection = [8000,9000,10000]
    for i in range(randomAsciiFromItem(selection)):
        data.append(row)
    return convert2DList(data,',')

if __name__ == "__main__":
    main()

