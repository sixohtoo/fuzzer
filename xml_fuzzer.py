import xml_utils as u
import random
import multiprocessing as mp
import xml.etree.ElementTree as et
from pwn import *

class Runner:
    def __init__(self, binary):
        """
        Initialise the binary file to be run.
        """
        self.binary = binary

    def run(self, input):
        """
        Run the binary with the given input and 
        return process status: PASS or FAIL
        """
        p = process(self.binary)
        p.sendline(input.encode('UTF-8'))
        p.shutdown()
        exit_code = p.poll(block=True)
        p.stdout.close()
        p.stderr.close()

        return exit_code


class XML_Fuzzer:
    def __init__(self, binary, input):
        """
        Initialise the binary file to be run and 
        input to be fuzzed.
        """
        super().__init__()
        self.binary = binary
        self.input = input
        self.runner = Runner(self.binary)
    
    def check_type(self):
        """
        Check if the input is in valid xml form.
        """
        try:
            et.fromstring(self.input)
        except et.ParseError:
            return False
        else:
            return True

    def run(self):
        """
        Run the binary with the given input 
        if the string input is in valid xml form.
        """
        if self.check_type() == True:
            return self.runner.run(self.input)
    
    def fuzz(self):
        """
        Fuzz the valid input and the mutated input 
        until the program catches a SEGFAULT: exit != 0.
        """
        xml = et.fromstring(self.input)

        while True:
            exit_code = self.run()
            
            # Return if there's a segfault
            ret_input = self.input
            if exit_code != 0:
                return (ret_input, exit_code)
            
            # Keep mutating
            xml = self.mutate(xml)
            self.input = et.tostring(xml).decode()


    def mutate(self, xml):
        """
        Mutate the given xml by different mutators, 
        then return the mutated xml.
        """
        mutators = [u.bits_flip, u.bytes_replace]

        for child in xml.iter():
            # Mutate the attributes of the current child
            attributes = child.items()
            mutator = random.choice(mutators)
            for a in attributes:
                child.set(a[0], mutator(a[1]))

            # Mutate the text of the current child iff
            # the modification won't violate xml parsing
            if not u.check_tag(child.tag):
                mutator = random.choice(mutators)
                child.text = mutator(child.text)
        
        return xml


if __name__ == '__main__':
    valid_input = "./bin/xml1.txt"
    binary = "./bin/xml1"

    with open(valid_input, "r") as f:
        input = f.read().strip()
    
    fuzzer = XML_Fuzzer(binary, input)
    # print(fuzzer.check_type())
    # xml = et.fromstring(input)
    # xml = fuzzer.mutate(xml)
    # xmlstr = et.tostring(xml).decode()
    # print(xmlstr)
    print(fuzzer.fuzz())

    # print(fuzzer.check_type())