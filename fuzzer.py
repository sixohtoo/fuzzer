#!/usr/bin/env python3

from pwn import *
import sys
import logging
import json
import xml
import csv


def main(binary, input_text):
	
	if check_json(input_text):
		# fuzz_json(sys.argv[1], sys.argv[2])
		print('Input file is a json')

		# TODO
		pass
	elif check_xml(input_text):
		# fuzz_xml(bytes)
		pass
	elif check_csv(input_text):
		print('Input file is CSV')

		# TODO
		# fuzz_csv(bytes)
		pass
	else:
		print('Input file is not a valid file type')
		# fuzz_plaintext(bytes)
		pass

def check_json(input_text):
	try:
		reader = json.load(input_text)
	except:
		return False
	
	return True

def check_xml(input_text): # TODO
	return False
	# try:
	# 	return xml.
	# except:
	# 	return False

def check_csv(input_text): # TODO needs to be more robust (thinks xml is csv)
	try:
		reader = csv.reader(input_text, delimiter=',')
	except:
		return False

	return True


if __name__ == '__main__':
	# sys.stdout = open("out", "w")

	try:
		binary = sys.argv[1]
		input_file = sys.argv[2]
		input_text = open(input_file, "r")
		print(binary)
		print(input_file)
		main(binary, input_text)
	except:
		print('Usage: ./fuzzer program sampleinput.txt')

	# sys.stdout.close()
