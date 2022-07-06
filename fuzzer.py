#!/usr/bin/env python3

from pwn import *
import sys
import logging
import json
import xml


def main():
	logging.info("beans")
	# bytes = b''
	# with open(sys.argv[2], "rb") as f:
	# 	bytes = f.read()

	if check_json(bytes):
		# fuzz_json(sys.argv[1], sys.argv[2])
		pass
	elif check_xml(bytes):
		# fuzz_xml(bytes)
		pass
	elif check_csv(bytes):
		# fuzz_csv(bytes)
		pass
	else:
		# fuzz_plaintext(bytes)
		pass

def check_json(text):
	return False
	# try:
	# 	return json.loads(text)
	# except:
	# 	return False

def check_xml(text):
	return False
	# try:
	# 	return xml.
	# except:
	# 	return False

def check_csv(text):
	return False



if __name__ == '__main__':
	sys.stdout = open("out", "w")
	main()
	sys.stdout.close()
