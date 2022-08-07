#!/usr/bin/env python3
import json
import random
import utils as u
import time
from math import pi
import multiprocessing as mp
from functools import partial
from pwn import *
import os
import itertools

MAX_INT = 2147483647
MIN_INT = -2147483648

lock = mp.Lock()

def fuzz_json(prog_name, text, lock, option):
    option %= 6

    data = json.loads(text)
    field = u.get_random_field(data)
    final = ''
    if option == 0:
        add_field(data)
        final = json.dumps(data)
    elif option == 1:
        remove_field(data, field)
        final = json.dumps(data)
    elif option == 2:
        data[field] = flip_bits(data[field])
        final = json.dumps(data)
    elif option == 3:
        swap_type(data, field)
        final = json.dumps(data)
    elif option == 4:
        smart_swap(data, field)
        final = json.dumps(data)
    elif option == 5:
        final = mutate_raw_string(text)
    
    payload = final
    p = process(prog_name, level='critical', timeout=1.5)
    p.sendline(payload.encode('utf-8'))

    p.proc.stdin.close()
    exit_code = p.poll(True)
    # Return if detected hangs/infinite loops
    if exit_code is None:
        print("Detected hangs/infinite loops. Program terminated")
        return 

    if exit_code == -11:
        with lock:
            with open("bad.txt", "w") as f:
                f.write(final)
    p.close()


    

def add_field(data):
    data['admin'] = 'something (may change this later)'
    data['another'] = 602.602

def remove_field(data, field):
    del data[field]

def flip_bits(current):
    if isinstance(current, int):
        bits = bin(current)
        return int(u.flip_bits(bits[2:]), 2)
    elif isinstance(current, str):
        bits = u.str_to_bits(current)
        return u.bits_to_str(u.flip_bits(bits))

def swap_type(data, field):
    '''
    types: int, string, list, empty list, dict, empty dictionary, bool
    '''
    option = random.randrange(0, 8)

    current = data[field]
    if option == 0: # int
        data[field] = 3
    elif option == 1: # string
        data[field] = "hello world"
    elif option == 3:
        data[field] = [1, 2, "hello"]
    elif option == 4:
        data[field] = []
    elif option == 5:
        data[field] = {
            'a' : 'hello',
            1 : option % 3,
            True : False,
            None : ['a', 3, None],
            3.1 : {'a' : 4}
        }
    elif option == 6:
        data[field] = {}
    elif option == 7:
        data[field] = True


def smart_swap(data, field):
    current = data[field]
    if isinstance(current, int):
        smart_swap_int(data, field)
    elif isinstance(current, str):
        smart_swap_string(data, field)

# Fields expects a number, so try
# int, double, negative number, 0, large number, small number, irrational number
def smart_swap_int(data, field):
    option = random.randrange(0, 10)
    current = data[field]
    if option == 0:
        data[field] = int(current)
    elif option == 1:
        data[field] = current * 1.0
    elif option == 2:
        data[field] = current * -1
    elif option == 3:
        data[field] = 0
    elif option == 4:
        data[field] = MAX_INT
    elif option == 5:
        data[field] = MIN_INT
    elif option == 6:
        data[field] = pi
    elif option == 7:
        data[field] = MAX_INT + 1
    elif option == 8:
        data[field] = MIN_INT - 1
    elif option == 9:
        data[field] = str(current)

# Field expects a string, so try
# normal string, large string, byte string, add random \s, add ", " and `, empty string
def smart_swap_string(data, field):
    option = random.randrange(0, 8)
    current = data[field]
    length = random.randrange(1, 10000)
    if option == 0:
        data[field] = str(current)
    elif option == 1:
        data[field] = u.generate_string(length)
    elif option == 2:
        data[field] = str(u.generate_bytes(length))
    elif option == 3:
        # Adds a \ every 3rd character
        for i in range(len(current)):
            if i % 3 == 0:
                current = u.insert_into_string(current, i, '\\')
        data[field] = current
    elif option == 4:
        # Adds a quote every 3rd character
        chars = ['\'', '\"', '`']
        for i in range(len(current)):
            if i % 3 == 0:
                current = u.insert_into_string(current, i, random.choice(chars))
        data[field] = current
    elif option == 5:
        # Adds a % every 3rd character (or a %n or %p)
        chars = ['%', '%', '%', '%n', '%p']
        for i in range(len(current)):
            if i % 3 == 0:
                current = u.insert_into_string(current, i, random.choice(chars))
    elif option == 6:
        data[field] = ""
    elif option == 7:
        byte = random.randrange(0, 255)
        data[field] = p8(byte)

def mutate_raw_string(text):
    """
        Mutating raw json string strategies
        0. flip random bits
        1. append random bytes after jsonobject
        2. append jsonobject after random bytes
        3. empty string
        4. duplicate entire string
        5. duplicate random section
        6. replace all " with ' (breaks it for some reason)
        7. replace all ' with "
        8. Delete random " or '
    """
    option = random.randrange(0, 10)
    if option == 0:
        return flip_bits(text)
    elif option == 1:
        return text + str(u.generate_bytes(15))
    elif option == 2:
        return str(u.generate_bytes(15)) + text
    elif option == 3:
        return ''
    elif option == 4:
        return text + text
    elif option == 5:
        start = random.randrange(0, len(text))
        end = random.randrange(start, len(text))
        copy = text[start:end]
        return text[:end] + copy + text[end:]
    elif option == 6:
        return text.replace("\"", "\'")
    elif option == 7:
        return text.replace("\'", "\"")
    elif option == 8:
        replace = set(['\'', '\"'])
        new = ""
        for letter in text:
            if letter in replace and random.randrange(0, 3) == 0:
                continue
            new += letter
        return new
    elif option == 9:
        c = random.randrange(32, 127)
        repeat = random.randrange(200, 1000)
        ret = f'{{{chr(c) * repeat}}}'
        return ret