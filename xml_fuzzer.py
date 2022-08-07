import xml_utils as u
import sys
import random
import xml.etree.ElementTree as et
from pwn import *

class Runner:
    def __init__(self, binary):
        """
        Initialisation:
        self.binary -> binary file to be run
        """
        self.binary = binary

    def run(self, input):
        """
        Run the binary with the given input and 
        return process exit code.
        """
        p = process(self.binary, timeout=1.5, level="critical")
        p.sendline(input.encode('UTF-8'))
        p.shutdown()
        exit_code = p.poll(block=True)
        p.stdout.close()
        p.stderr.close()

        return exit_code

class XML_Fuzzer:
    def __init__(self, binary, input):
        """
        Initialisation: 
        self.binary -> binary file to be run
        self.input -> xml string to be fuzzed
        self.runner -> runner object (run the program)
        """
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
            # print(self.input)
            return self.runner.run(self.input)
    
    def fuzz(self):
        """
        Fuzz the valid input and the mutated input 
        until the program catches a SEGFAULT: exit != 0.
        """
        xml = et.fromstring(self.input)

        while True:
            exit_code = self.run()

            # Return if detected hangs/infinite loops
            if exit_code is None:
                print("Detected hangs/infinite loops. Program terminated")
                return 

            # Return if there's a segfault
            ret_input = self.input  
            if exit_code == -11:
                with open("bad.txt", "w") as f:
                    f.write(ret_input)
                break

            # if exit_code != 0:
            #     if exit_code == -11:
            #         print(f"Exit code: {exit_code}, Status: Found a SEGFAULT!\n")
            #     else:
            #         print(f"Exit code: {exit_code}, Status: Unknown Error\n")
            #     return (ret_input, exit_code)
            # else:
            #     print(f"Exit code: {exit_code}, Status: Success\n")
            
            # Keep mutating
            xml = self.mutate(xml)
            self.input = et.tostring(xml).decode()

    def mutate(self, xml):
        """
        Mutate the given xml input by changing bytes of 
        both attributes and texts, and adding new DOM elements,
        then return the mutated xml.
        """
        added_element = False

        for child in xml.iter():
            # Mutate the attributes of the current child
            # only if the element isn't added by us
            if(child.get("added") != "yes"):
                attributes = child.items()
                for a in attributes:
                    child.set(a[0], u.bytes_replace(a[1]))

            # Mutate the text of the current child only if
            # the modification won't violate xml parsing
            if u.check_text_modification(child.tag):
                child.text = u.bytes_replace(child.text)

            # Adding new DOM elements only if
            # only if the element hasn't added by us and 
            # the chance of  modifying < 1/4 and 
            # the modification is necessary
            p = random.randint(0, 100)
            if not added_element and p < 25:
                if u.check_element_modification(child.tag) and (child.get("added") != "yes"): 
                    choices = [fc.value for fc in u.ELEMENTS]
                    new_element = et.fromstring(random.choice(choices)) 
                    # child.append(et.fromstring(new_element))
                    child = u.add_elements(child, new_element)
                    added_element = True

        return xml