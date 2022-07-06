#!/usr/bin/env python3
import json
import random
from utils import *

MAX_INT = 2147483647
MIN_INT = -2147483648

def fuzz_json(prog_name, input_name):
    with open(input_name, "r") as f:
        data_raw = f.read()
    for _ in range(10):
        data = json.loads(data_raw)

    

def add_field(data):
    data['admin'] = 'something (may change this later)'
    data['another'] = 602.602

def remove_field(data):
    del data[get_random_field(data)]

def flip_bits(data):
    pass

def swap_type(data):
    '''
    types: int, string, list, dictionary, nothing
    '''
    pass

def smart_swap(data):
    field = get_random_field(data)
    current = data[field]
    if isinstance(current, int):
        smart_swap_int(data, field)
    elif isintance(current, str):
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
        data[field] = math.PI
    elif option == 7:
        data[field] = MAX_INT + 1
    elif option == 8:
        data[field] = MIN_INT - 1
    elif option == 9:
        data[field] = str(current)

# Field expects a string, so try
# normal string, large string, byte string, add random \s, add ", " and `, empty string
def smart_swap_string(data, field):
    option = random.randrange(0, 5)
    current = data[field]
    length = random.randrange(1, 10000)
    if option == 0:
        data[field] = str(current)
    elif option == 1:
        data[field] = generate_string(length)
    elif option == 2:
        data[field] = generate_bytes(length)
    elif option == 4:
        # Adds a \ every 3rd character
        for i in range(len(current)):
            if i % 3 == 0:
                current = insert_into_string(current, i, '\\')
        data[field] = current
    elif option == 5:
        # Adds a quote every 3rd character
        chars = ['\'', '\"', '`']
        for i in range(len(current)):
            if i % 3 == 0:
                current = insert_into_string(current, i, random.choice(chars))
        data[field] = current
    elif option == 6:
        data[field] = ""


if __name__ == '__main__':
    fuzz_json("a", "bin/json1.txt")