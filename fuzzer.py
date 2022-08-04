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
import time


lock = mp.Manager().Lock()

def main():

	if len(sys.argv) != 3:
		sys.exit("Usage: ./fuzzer program sampleinput.txt")

	try:
		text = open(sys.argv[2], "r")
	except:
		print("Error:", sys.exc_info()[0])
		sys.exit("Usage: ./fuzzer program sampleinput.txt")

	start = time.time()

	if check_json(text):
		print('File is json')
		function = json_fuzzer.fuzz_json
	elif check_csv(text):
		print('File is csv')
		function = csvFuzzer.fuzz_csv
	else:
		print('IDK')
		exit(0)
	input_text = open(sys.argv[2], "r").read()
	with mp.Pool(20) as p:
		p.map(partial(function, sys.argv[1], input_text, lock), range(100000))



def check_json(text):
	text.seek(0)

	try:
		json.loads(text.read().strip())
	except:
		return False

	return True

def check_xml(text):
	return text[0] == '<'

def check_csv(text):
	# Move to the start of the file
	text.seek(0)

	lines = text.readlines()
	commas = lines[0].count(",") # count the commas and see if there's the same amount on each line

	if len(lines) <=1 or commas == 0:
		return False

	for line in lines:
		if line.count(",") != commas:
			return False

	return True


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
	# lock = mp.Manager().Lock()

	main()
