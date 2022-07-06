#!/usr/bin/env python3

import random
import time
from io import BytesIO
from pwn import *

# Generates length many random bytes and returns a bytestring
def generate_bytes(length):
	b = BytesIO()
	for i in range(0, length):
		b.write(p8(random.randrange(0, 255)))
	b.seek(0)
	return b.read()

# Generates length many random bytes and returns a bytestring
def generate_string(length):
	return 'A' * length

# Returns name of a random field inside data dictionary
def get_random_field(data):
	return data.keys()[random.randrange(0, len(data))]

def insert_into_string(string, index, char):
	return string[:index] + char + string[index:]

if __name__ == '__main__':
	# for i in range(100):
		# print(generate_plaintext(i))
	generate_bytes()