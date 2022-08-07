#!/usr/bin/env python3

from pwn import *
import sys
import logging
import json 
import xml
import json_fuzzer
import csvFuzzer
import xml_fuzzer
import jpeg_fuzzer
import plaintext_fuzzer
import multiprocessing as mp
from functools import partial
import csv
import time
import xml.etree.ElementTree as et


lock = mp.Manager().Lock()

def main():

	if len(sys.argv) != 3:
		sys.exit("Usage: ./fuzzer program sampleinput.txt")

	try:
		# text = open(sys.argv[2], "rb").read()
		with open(sys.argv[2], "rb") as f:
			text = f.read()
	except:
		print("Error:", sys.exc_info()[0])
		sys.exit("Usage: ./fuzzer program sampleinput.txt")

	start_time = time.time()

	if check_xml(text):
		print('File is xml')
		input_text = open(sys.argv[2], "r").read()
		fuzzer = xml_fuzzer.XML_Fuzzer(sys.argv[1], input_text)
		fuzzer.fuzz()
	else:
		if check_json(text):
			print('it json!?!?!')
			function = json_fuzzer.fuzz_json
			text = text.decode('utf-8')
		elif check_csv(text):
			print('it csb!>>!')
			function = csvFuzzer.fuzz_csv
			text = text.decode('utf-8')
		elif check_jpg(text):
			function = jpeg_fuzzer.fuzz_jpeg
			print('it jpg it jpg')
		else:
			print('File is plaintext')
			text = text.decode('utf-8')
			function = plaintext_fuzzer.fuzz_plaintext

	# input_text = open(sys.argv[2], "r").read()
		with mp.Pool(20) as p:
			p.map(partial(function, sys.argv[1], text, lock), range(10000))

	print('Fuzzing done')

	end_time = time.time()

	print('Fuzzer ran for ' + str(end_time-start_time) + ' seconds.')



def check_json(text):
	try:
		json.loads(text)
	except:
		return False

	return True

def check_xml(text):
	# text = text.read()
	try:
		et.fromstring(text)
	except et.ParseError:
		return False
	else:
		return True

def check_csv(text):
	# Move to the start of the file

	# lines = text.readlines()
	lines = text.split(b'\n')
	if lines[-1] == b'':
		lines = lines[:-1]

	commas = lines[0].count(b",") # count the commas and see if there's the same amount on each line

	if len(lines) <=1 or commas == 0:
		return False

	for line in lines:
		if line.count(b",") != commas:
			return False

	return True

def check_jpg(text):
	return text[:12] == b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01"


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
