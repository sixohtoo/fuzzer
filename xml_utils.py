"""
This file contains all the required helper functions for  
xml fuzzer.
"""
import re
import random
from enum import Enum

class FUZZ_CONSTANTS(Enum):
    """
    All the constants that are required for fuzzing lie here.
    """
    # Known integers
    MAX_INT = "2147483647"
    MIN_INT = "-2147483648"
    EXCEED_MAX_INT = "2147483648"
    EXCEED_MIN_INT = "-2147483649"
    ZERO = "0"
    ONE = "1"
    NEGATIVE_ONE = "-1"

    # Edge cases for string
    EMPTY_STRING = ""
    BAD_URL = "http://wesifolrhurqewiop;fhjewquoipfhjuqweo.dsh"

    # Format strings for potential vulnerability exploits
    FORMAT_STRING1 = "%s"
    FORMAT_STRING2 = "%d"
    FORMAT_STRING3 = "%x"
    FORMAT_STRING4 = "%p"

    # Special characters for xml
    SPECIAL_CHAR1 = "&"
    SPECIAL_CHAR2 = "<"
    SPECIAL_CHAR3 = ">"
    SPECIAL_CHAR4 = "'"
    SPECIAL_CHAR5 = '"'

class ELEMENTS(Enum):
    """
    All the necessary DOM elements to be added lie here. 
    """
    # Basic XML/HTML DOM elements
    DIV = '<div added="yes" id="yes"><a added="yes" href="http://nowebsite.com">Nothing</a><link added="yes" href="http://nowebsite.com" /><span added="yes">text</span></div>'
    SPAN = '<span added="yes">Nothing</span>'
    A = '<a added = "yes" href="http://nowebsite.com">Nothing</a>'
    P = '<p added="yes">Nothing</p>'

    # Basic DOM elements with many attributes
    DIV_ATTRIBUTES = '<div added="yes" id="yes" a1="idk" a2="idk" a3="idk"></div>'
    SPAN_ATTRIBUTES = '<span added="yes" a1="idk" a2="idk" a3="idk"></span>'
    A_ATTRIBUTES = '<a added = "yes" href="http://nowebsite.com" a1="idk" a2="idk" a3="idk"></a>'
    P_ATTRIBUTES = '<p added="yes" a1="idk" a2="idk" a3="idk"></p>'

def bits_flip(str):
    """
    Flipping bits of the given string.
    """
    # Can't flip an empty string
    if str == "":
        return str

    # Convert the string into binary
    bits = string_to_binary(str)
    length = len(bits)

    # Bit flipping via XOR: 0 -> 1 and 1 -> 0
    xor_bits = "1" * length
    bits = int(bits, 2)
    xor_bits = int(xor_bits, 2)
    flipped = bin(bits ^ xor_bits)

    # Formatting 
    flipped = flipped[2:]
    flipped = flipped.zfill(length)

    flipped_string = binary_to_string(flipped)

    return flipped_string

def string_to_binary(str):
    """
    Convert the given string into binary form.
    """
    return ''.join(f"{ord(i):08b}" for i in str)

def binary_to_string(bin):
    """
    Convert the given binary into a string.
    """
    # Split the binary by 1 byte  (8 bits) each
    format  = "." * 8
    bins = re.findall(format, bin)
    str = ""
    
    for b in bins:
        b_int = int(b, 2)
        char = chr(b_int)
        str += char
    
    return str

def generate_bstring(n):
    """
    Generate a byte string with length n.
    """
    return "A" * n

def bytes_replace(str):
    """
    Return a string with random length, 
    or any pre-defined fuzzed constants.
    """
    choices = [fc.value for fc in FUZZ_CONSTANTS]
    length = random.randint(1,10000)
    choices.append(generate_bstring(length))

    choose = random.choice(choices)
    return choose 

def check_text_modification(tag):
    """
    Check if the text modification of the given tag
    is valid.
    """
    # Tags that their text cannot be modified
    # Modifying their text will result in xml parse error
    tags = ["root", "html", "head","link", "body", "div", "tail"]

    if tag in tags:
        return False
    return True

def check_element_modification(tag):
    """
    Check if the adding element to the given tag 
    is  necessary.
    """
    # Adding elements to these tag is useless and 
    # increase the time to find a bug
    tags = ["root", "html", "head", "link", "body", "a", "h1", "tail"]

    if tag in tags:
        return False
    return True
