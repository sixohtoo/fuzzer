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
	fields = [x for x in data]
	return fields[random.randrange(0, len(data))]

def insert_into_string(string, index, char):
	return string[:index] + char + string[index:]

def flip_bits(bits):
	# print("flipping", bits)
	# print("len", len(bits))
	arr = [x for x in bits]

	freq = random.randrange(1, len(bits) + 1)
	# print("freq", freq)
	for i in range(len(arr)):
		if (i + 1) % freq == 0:
			# print('e')
			arr[i] = '0' if int(arr[i]) else '1'
	return ''.join(arr)
	# arr = bits.split(" ")
	# print(arr)

def str_to_bits(text):
	return ''.join(format(i, '08b') for i in bytearray(text, encoding ='utf-8'))

def bits_to_str(bits):
	return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(bits)]*8))

if __name__ == '__main__':
	x = 5
	bits = bin(x)
	flipped = flip_bits(bits[2:])
	print(flipped)
	print(int(bits, 2))
	print(int(flipped, 2))
	
	# for i in range(100):
		# print(generate_plaintext(i))
	# s = 'hello'
	# bits = str_to_bits(s)
	# flipped = flip_bits(bits)
	# print(bits_to_str(bits))
	# print(bits_to_str(flipped))