#!/usr/bin/env python3

import time
from utils import generate_bytes
import multiprocessing as mp
import subprocess as sub
from pwn import *

lock = mp.Lock()

def func(length):
	p = process(f'bin/plaintext2', level='critical')
	payload = generate_bytes(length)
	p.sendline(payload)
	p.wait_for_close()
	if p.poll() != 0:
		with lock:
			print(payload)



def main():
	with mp.Pool(20) as p:
		p.map(func, range(100))

out = open("out", "w")
sys.stdout = out
if __name__ == '__main__':
	main()
	out.close()