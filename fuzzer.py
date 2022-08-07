#!/usr/bin/env python3

from pwn import *
import sys
import logging
import json
import xml.etree.ElementTree as et
import json_fuzzer
import csvFuzzer
import xml_fuzzer
import plaintext_fuzzer
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
		input_text = open(sys.argv[2], "r").read()
	except:
		print("Error:", sys.exc_info()[0])
		sys.exit("Usage: ./fuzzer program sampleinput.txt")

	start_time = time.time()

	if check_xml(text):
		print('File is xml')
		fuzzer = xml_fuzzer.XML_Fuzzer(sys.argv[1], input_text)
		fuzzer.fuzz()
	else:
		if check_json(text):
			print('File is json')
			function = json_fuzzer.fuzz_json
		elif check_csv(text):
			print('File is csv')
			function = csvFuzzer.fuzz_csv
		else:
			print('File is plaintext')
			function = plaintext_fuzzer.fuzz_plaintext

		# input_text = open(sys.argv[2], "r").read()
		with mp.Pool(20) as p:
			# for i in range(0,10):
				# sys.settrace(tracing)
			# p.apply_async(function, sys.argv[1], input_text, lock, i)
			p.map(partial(function, sys.argv[1], input_text, lock), range(10))
				# sys.settrace(None)

	print('Fuzzing done')

	end_time = time.time()

	print('Fuzzer ran for ' + str(end_time-start_time) + ' seconds.')



def check_json(text):
	text.seek(0)

	try:
		json.loads(text.read().strip())
	except:
		return False

	return True

def check_xml(text):
	text = text.read()
	try:
		et.fromstring(text)
	except et.ParseError:
		return False
	else:
		return True

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

# all_coverage = []
# csv_mutators = ["addLines", "modifiedData", "setToNone", "flipBits"]
# json_mutators = ["add_field",  "remove_field", "flip_bits", "smart_swap_int", "smart_swap_string", "mutate_raw_string"]
# xml_mutators = ["bytes_replace", "add_elements"]
# plaintext_mutators = ["generate_random_string", "generate_random_ascii", "generate_random_number"]

# all_mutators = []
# all_mutators += csv_mutators
# all_mutators += json_mutators
# all_mutators += xml_mutators
# all_mutators += plaintext_mutators

# def tracing(frame, event, args):
# 	if event == 'line':
# 		function_name = frame.f_code.co_name
# 		# line = frame.f_lineno
# 		if function_name in all_mutators:
# 			print(function_name)
# 		# 	all_coverage.append(function_name)
# 	return tracing

#     # return tracing

if __name__ == '__main__':

	# lock = mp.Manager().Lock()
	# sys.settrace(tracing)
	main()
	# sys.settrace(None)
	# print(set(all_coverage))
