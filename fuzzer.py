#!/usr/bin/env python3

from pwn import *
import sys
import logging
from input_checks import check_json, check_csv, check_xml
from json_fuzzer import fuzz_json
from runner import runner

def main(binary, input_text):
	
	if check_json(input_text):
		print('Input file is a json')
		# fuzz_json(binary, input_text, 1) # Not sure what option is here so just put 0
		runner(binary, input_text, 0)
		# TODO
		
	elif check_xml(input_text):
		# fuzz_xml(bytes)
		pass
	elif check_csv(input_text):
		print('Input file is CSV')

		# TODO
		# fuzz_csv(bytes)
		pass
	else:
		print('Input file is not a valid file type(yet)')
		# fuzz_plaintext(bytes)
		pass


if __name__ == '__main__':
	# sys.stdout = open("out", "w")

	if(len(sys.argv) != 3):
		sys.exit('Usage: ./fuzzer program sampleinput.txt')

	try:
		binary = sys.argv[1]
		input_text = open(sys.argv[2], "r")
		
	except:
		sys.exit('Usage: ./fuzzer program sampleinput.txt')
	main(binary, input_text)
	# sys.stdout.close()
