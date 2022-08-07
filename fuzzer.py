#!/usr/bin/env python3

from pwn import *
import sys
import logging
import json 
import xml
import json_fuzzer
import csvFuzzer
import jpeg_fuzzer
import multiprocessing as mp
from functools import partial
import csv
import time


lock = mp.Manager().Lock()


def main():
	with open(sys.argv[2], "rb") as f:
		text = f.read()

	if check_json(text):
		function = json_fuzzer.fuzz_json
		text = text.decode('utf-8')
	elif check_csv(text):
		function = csvFuzzer.fuzz_csv
		text = text.decode('utf-8')
	elif check_jpg:
		function = jpeg_fuzzer.fuzz_jpeg
		# text = text.encode('utf-8')
		print('it jpg it jpg')
	else:
		text = text.decode('utf-8')
		print('idk wtf this is')

	print("===========================================================")
	print(f"Fuzzer started at: {time.ctime(time.time())}")
	print("===========================================================")

	with mp.Pool(20) as p:
		p.map(partial(function, sys.argv[1], text, lock), range(100000))


def check_json(text):
	try:
		return json.loads(text)
	except:
		return False

def check_xml(text):
	return text[0] == b'<'

def check_csv(text):
	return False

def check_jpg(text):
	return text[:12].encode('utf-8') == b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01"


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
