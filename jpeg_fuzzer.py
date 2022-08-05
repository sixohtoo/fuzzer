#!/usr/bin/env python3

import random
from pwn import *
import utils

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

num_special = len(special_bytes)

magic_bytes = [
    b"",                                                 # text file
    b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01", # jpeg
    b"\x1f\x1d",                                         # tar LZH algorithm
    b"\x42\x5a\x68",                                     # bz2
    b"\x47\x49\x46\x38\x37\x61",                         # gif
    b"\x46\x4F\x52\x4d\xde\xad\xbe\xef\x41\x49\x46\x46", # Audio Interchange File Format
    b"\x4c\x5a\x49\x50",                                 # lzip
    b"\x50\x4b\x03\x04",                                 # zip
    b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a",                 # png
    b"\x25\x50\x44\x46\x2d",                             # pdf
    b"\x52\x49\x46\x46\xde\xad\xbe\xef\x57\x41\x56\x45", # wav
    b"\xff\xfb",                                         # mp3
    b"\x7f\x45\x4c\x46",                                 # elf
]

num_magic = len(magic_bytes)

def fuzz_jpeg(prog_name, text, lock, option):
    option %= len(mutators)
    text = mutators[option](text)

    if text == None:
        print(option)
    p = process(prog_name, level='critical')
    p.sendline(text)

    p.proc.stdin.close()
    if p.poll(True) == -11:
        with lock:
            print('yay')
            with open("bad.txt", "w") as f:
                f.write(final)
    p.close()

def swap_special_bytes(text):
    old_byte = special_bytes[random.randrange(0, num_special)]
    new_byte = special_bytes[random.randrange(0, num_special)]
    return text.replace(old_byte, new_byte)

def remove_special_bytes(text):
    special = special_bytes[random.randrange(0, num_special)]
    return text.replace(special, b'')

def edit_magic_bytes_smart(text):
    new_magic_bytes = magic_bytes[random.randrange(0, num_magic)]
    return new_magic_bytes + text[12:]

def smart_changes(text):
    option = random.randrange(0, 3)
    
    """
    0: Return start bytes and end bytes
    1: Return end bytes before start bytes
    2: Swap end bytes and start bytes
    """

    if option == 0:
        return magic_bytes[1] + special_bytes[-1]
    elif option == 1:
        return special_bytes[-1] + text
    elif option == 2:
        return special_bytes[-1] + text[12:-4] + magic_bytes[1]
    # elif option == 3:
    #     # print('woir?')
    #     return str(int(text, 16))


def replace_bytes(text):
    target = utils.generate_bytes(2)
    return text.replace(target, b'')

def insert_random_bytes(text):
    random_byte = utils.generate_bytes(1)
    location = random.randrange(12, len(text))
    # text[location] = random_byte
    # return text
    return text[:location] + random_byte + text[location:]

def insert_0xff_bytes(text):
    location = random.randrange(12, len(text))
    return text[:location] + b'\xff' + text[location:]

def reverse_bytes(text):
    location = random.randrange(len(text))
    size = random.randrange(len(text) - location)
    return text[:location] + text[location : location + size:-1] + text[location + size:]

mutators = {
    0: swap_special_bytes,
    1: remove_special_bytes,
    2: edit_magic_bytes_smart,
    3: smart_changes,
    4: replace_bytes,
    5: insert_random_bytes,
    6: insert_0xff_bytes,
    7: reverse_bytes
}
# if __name__ == '__main__':
#     fuzz_jpeg(prog_name, text, lock, option)()