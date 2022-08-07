#!/usr/bin/env python3

import sys
import time
import multiprocessing as mp
import subprocess as sub
from itertools import permutations
from pwn import *
import utils as u

lock = mp.Lock()

def fuzz_plaintext(prog_name, text, lock, option):
	option %= 4
	p = process(prog_name, level = 'critical')
	
	input_text = text.split()
	if option == 0:
		# generate a payload of a standard string longer than the input text
		payload = generate_random_string(random.randrange(0 , 10000))
	elif option == 1:
		payload = generate_random_ascii(random.randrange(0, 10000))
	elif option == 2:
		payload = generate_random_number(random.randrange(0, 10000))
	elif option == 3:
		payload = flip_bits(input_text[random.randrange(len(input_text))])


	# If the input text is just 1 line then we just send our payload
	if len(input_text) == 1:
		p.sendline(payload.encode('utf-8'))

		error_code = p.poll(True)

		if error_code == -11:
			with lock:
				with open("bad.txt", "w") as f:
					f.write(payload)

		p.close()
	else:
		# Generate combinations of each line of input and the payload
		num_inputs = len(input_text)

		# choose one of the inputs to be replaced by the payload

		replace = random.randrange(num_inputs)
		input_text[replace] = payload

		for i in input_text:
			p.sendline(i.encode('utf-8'))

			sleep(0.1)

			error_code = p.poll()
			if error_code is not None:
				if error_code == -11:
					with lock:
						with open("bad.txt", "w") as f:
							for line in input_text:
								f.write(line + '\n')
				break
		p.close()
	# Get paths from the given text

	# for line in input_text:
	# 	print(line)
	# 	p.sendline(line.encode())

	# 	sleep(0.1)
	# 	error_code = p.poll()
	# 	print(error_code)
	# 	if error_code == None:
	# 		paths.append(line)
	# print(paths)
	

	# get the good inputs
	# get code paths from good inputs(coverage)
	# mutate the last input
	
def generate_random_string(length):
	return ''.join(random.choice(string.printable) for i in range(length))	


def generate_random_ascii(length):
	return ''.join(random.choice(string.ascii_letters) for i in range(length))	

def generate_random_number(num_range):
	return str(random.randint(-num_range, num_range))

def flip_bits(sample_input):
    return u.bits_to_str(u.flip_bits(u.str_to_bits(sample_input)))

def keyword_addition(sample_input):
	sample_input += "admin"
	sample_input += "%d"
	sample_input += "password"
	return sample_input

def large_plaintext(sample_input):
	return sample_input + ("%d%n99999" * 999)


if __name__ == '__main__':

	binary = sys.argv[1]
	text = open(sys.argv[2], "r").read()
	print('Running plaintext fuzzer...')
	fuzz_plaintext(binary, text, lock, random.randrange(10000))