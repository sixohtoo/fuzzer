#!/usr/bin/env python3

from pwn import *
import sys
import logging
import json
import xml
import json_fuzzer
import csvFuzzer
import multiprocessing as mp
from functools import partial
import csv


lock = mp.Manager().Lock()

def main():
	with open(sys.argv[2], "r") as f:
		text = f.read()

	if check_json(text):
		function = json_fuzzer.fuzz_json
	else:
		function = csvFuzzer.fuzz_csv

	with mp.Pool(20) as p:
		p.map(partial(function, sys.argv[1], text, lock), range(1000))

def check_json(text):
	try:
		return json.loads(text)
	except:
		return False

def check_xml(text):
	return text[0] == '<'

def check_csv(text):

	return False


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

if __name__ == '__main__':
	main()
