#!/usr/bin/env python3

import random
import time
from io import BytesIO
from pwn import *

# Generates length many random bytes and returns a bytestring
def generate_bytes(length):
	# string_length = random.randrange(0, max_length + 1)
	b = BytesIO()
	# b.write(p8(0))
	# b.seek(0)
	# print(b.read())
	for i in range(0, length):
		b.write(p8(random.randrange(0, 255)))
	b.seek(0)
	return b.read()

if __name__ == '__main__':
	# for i in range(100):
		# print(generate_plaintext(i))
	generate_bytes()