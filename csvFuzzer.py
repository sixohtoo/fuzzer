#!/usr/bin/python3

import sys
import csv
import string
import random
import os
import time
from pwn import *
import utils as u
import io as ioModule
import time

sampleInput = "bin/csv1.txt"
sampleInput2 = "bin/csv2.txt"
start_time = time.time() 

def fuzz_csv(program, sampleInputText, lock, option):
    option %= 4
    sampleInput = convertCsvToList(sampleInputText)

    if option == 0:
        dataToSend = addLines(sampleInput)
    elif option == 1:
        dataToSend = modifiedData(sampleInput)
    elif option == 2:
        # send in nothing to program, ie simulate CTRL-D
        dataToSend = None
    elif option == 3:
        dataToSend = flipBits(sampleInput)
    io = process(program, level='critical')
    if (dataToSend != None):
        sendDataToPwnTwls(dataToSend,io)
    io.proc.stdin.close()
    exitCode = io.poll(block=True)
    if (exitCode == -11):
        log_vuln(start_time,time.time(),payload,vul_counter)
        with lock:
            with open("bad.txt", "w") as f:
                for line in dataToSend:
                    f.write(line + '\n')
    io.close()
 
# given a iterable list, send in each line of the list to a process in pwntools
def sendDataToPwnTwls(inputList,process):
    for line in inputList:
        process.sendline(line.encode('utf-8'))

# send CTRL-D to proram
# TODO: make it work
def sendEmptyToPwnTwls(process):
    process.sendline(b"\4")


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
def convertCsvToList(csvString):
    outputList = []
    f = ioModule.StringIO(csvString)
    for row in csv.reader(f,delimiter=','):
        outputList.append(row)
    return outputList

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
# ----------------------------------------- MUTATION FUNCTIONS -------------------------------------------- #
# TODO : return a modified version of the header in sampleInput
# def manipulateCSVheader(sampleInput):
#     modifiedHeader = []
#     sameData = []
#     with open(sampleInput, mode='r') as sampleInputFile:
#         for i,row in enumerate(csv.reader(sampleInputFile,delimiter=',')):
#             # changing the ascii characters of the header
#             for item in row:
#                 # only manipulate the header
#                 if i == 0:
#                     charToReplace = randomAsciiFromItem(item)
#                     if ( charToReplace in item):
#                         item = item.replace(charToReplace,randomAsciiGen())                      
#                         modifiedHeader.append(item)
#             if (i != 0):
#                 sameData.append(row)
#     return convert2DList(modifiedData,',')

# input 2d array
# output a random bit is changed 
def flipBits(sampleInput):
    row = randomAsciiFromItem(list(range(0,len(sampleInput))))
    col = randomAsciiFromItem(list(range(0,len(sampleInput[row]))))
    bits = u.str_to_bits(sampleInput[row][col])
    sampleInput[row][col] = u.bits_to_str(u.flip_bits(bits))


selection = ["%s","%n","A"*99, "%n"]
def modifiedData(sampleInput):
    modifiedData = sampleInput
    for i,row in enumerate(modifiedData):
        # changing the ascii characters of the input
            newRow = []
            for j,item in enumerate(row):
                # keep the header the same
                if i != 0:
                    item += randomAsciiFromItem(selection)
                    modifiedData[i][j] = item
    return convert2DList(modifiedData,',')

# send a modified delimiter ("\n,""(empty string),random char,%s")  
# TODO : fix eof in pwntools bug
def modifiedDelimiter(sampleInput):
    modifiedDelimiter = ["\n","","%","%n","%s","%d",randomAsciiGen()]
    return convert2DList(sampleInput, random.choice(modifiedDelimiter))

# add large amount of rows to the csvFile
def addLines(sampleInput):
    data = sampleInput
    rowSelection= ["%n","%d","%s","%p","%x"]
    rowToAdd = []
    # make a new row, with number of elements as large as the width
    for i in range(0,len(data[0])):
        rowToAdd.append(randomAsciiFromItem(rowSelection))
    # choose the number of times to loop over and add row of data
    selection = [50,100,150,200,250,300,350]
    for i in range(randomAsciiFromItem(selection)):
        data.append(rowToAdd)
    return convert2DList(data,',')


#------------------------------------------ Generating new input to fuzz ------------------------------------- #
# send in am empty file, with no elements
def emptyCsv():
    return []

# def largeColoum():
#     selection = [10,20,30,40,50,60,70,80,90,100]


if __name__ == "__main__":
    fuzz_csv("bin/csv1","bin/csv1.txt")
    fuzz_csv("bin/csv2","bin/csv2.txt")
