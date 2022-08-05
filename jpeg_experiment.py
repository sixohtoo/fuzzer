#!/usr/bin/env python3

from pwn import *
from copy import deepcopy
import utils


def main():
    # for i in range(2 ** 8 - 1):
        # for j in range(2 ** 8 - 1):
            with open("bin/jpg1.txt", "rb") as f:
                text = f.read()

            index = text.find(b'\xff\xc0')
            print(text[index:index + 18])
            text = text[:index] + b'\xff\xc0\x00\x11\x08\x01\xd6\x01\x84' + b'\x03' + b'\xde\x23' + text[index + 12:]
            #                           length      height
            # text = text[:index + 5] + b'\x00\x10' + b'\x2e\xe0' +  text[index + 9:]   
            # text = text[:index + 2] + b'\x00\x11\x08' + b'\x00\x05' + b'\x00\x05' + p8(3) + text[index + 10:]
            print(text[index:index + 18])

            # change length of huffman table
            # index = text.find(b'\xff\xc4')
            # print(text[index : index + 12])
            # text = text[:index + 2] + b'\x00\xee' + text[index + 4:]

            p = process("bin/jpg1", level='critical')
            p.sendline(text)
            # print(p.recv())
            p.proc.stdin.close()
            # print(p.recv())
            poll = p.poll(True)
            # print(word)
            x = p.recv().decode('utf-8')
            print(x)
            if poll == -11:
                print('yeee')
                with open('bad.txt', 'w') as e:
                    e.write(i)

            p.close()
            # if 'P6' in x:
            #     print("P6", i)
            # elif 'P5' in x:
            #     print("P5!!!!", i)
            # print("\n")


special_bytes = [
    b'\xff\xd8', # Start of Image
    b'\xff\xc0', # Start of Frame
    b'\xff\xc2', # Start of Frame
    b'\xff\xc4', # Define Huffman tables
    b'\xff\xdb', # Define quantization tables
    b'\xff\xdd', # Define restart interval
    b'\xff\xda', # Start of Scan
    b'\xff\xfe', # Comment
    b'\xff\xd9'  # End of Image
]

if __name__ == "__main__":
    main()

"""
works
c2

doesn't work
d8
c0

crashes

"""
