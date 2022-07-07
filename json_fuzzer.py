#!/usr/bin/env python3
import json
import random
import utils as u
import time
from math import pi

MAX_INT = 2147483647
MIN_INT = -2147483648


def fuzz_json(prog_name, input_name):
    with open(input_name, "r") as f:
        data_raw = f.read()
    option = 0
    while True:
        data = json.loads(data_raw)
        field = u.get_random_field(data)
        if option == 0:
            add_field(data)
        elif option == 1:
            remove_field(data, field)
        elif option == 2:
            flip_bits(data, field)
        elif option == 3:
            swap_type(data, field)
        elif option == 4:
            smart_swap(data, field)
            option = -1
        
        option += 1
        print(json.dumps(data, indent=2))
        # time.sleep(2)

    

def add_field(data):
    data['admin'] = 'something (may change this later)'
    data['another'] = 602.602

def remove_field(data, field):
    print('removing', field)
    del data[field]

# ''.join(format(i, '08b') for i in bytearray(test_str, encoding ='utf-8'))
# ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)]*8))
def flip_bits(data, field):
    current = data[field]
    print('flipping', field)
    if isinstance(current, int):
        bits = bin(current)
        data[field] = int(u.flip_bits(bits[2:]), 2)
    elif isinstance(current, str):
        bits = u.str_to_bits(current)
        data[field] = u.bits_to_str(u.flip_bits(bits))

# make this recursive somehow (lists inside of dicts inside of lists, etc)
# Maybe add function as a data type?
def swap_type(data, field):
    '''
    types: int, string, list, empty list, dict, empty dictionary, bool
    '''
    print('swapping', field)
    option = random.randrange(0, 8)
    print("chose option", option)
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
    print('smart swapping', field)
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
    print('smart string', field)
    print('chose option', option)
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
    option = random.randrange(0, 6)
    current = data[field]
    length = random.randrange(1, 10000)
    print('smart string', field)
    print('chose option', option)
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
        data[field] = ""


if __name__ == '__main__':
    fuzz_json("a", "bin/json1.txt")
    # a = 'hello'
    # a = u.generate_bytes(10)
    # print(a)
    # print(str(a))