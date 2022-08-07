Fuzzer
=========

### Design:

The fuzzer works by first detecting which type of input it’s given and then uses multithreading to call the input type’s respective fuzzer function, which mutates the input data, and runs the provided binary, where it passes in the mutated data through stdin. Currently, the methods used for speeding up the fuzzer are multithreading and reading the input data before the multithreading starts. This allows us to only open the input data file once, which avoids a lot of overhead.

Once the file type is chosen, it is then sent to the according method which randomly chooses a mutation strategy and mutates the input. 

### Features

Currently, the fuzzer can mutate json, csv, xml, plaintext and jpeg inputs. It uses mutation strategies specific to the input’s data type as well as some general mutation strategies that are applicable for any type of input.

### CSV Fuzzer

The csv fuzzer mutates the sample input based on three different strategies. This includes flipping random bits, randomly inserting format strings and adding large amounts of lines to a csv object. The strategy is then chosen randomly and sent to the program.

The main vulnerability stemming from the csv1 file is when the fuzzer calls the function addLines(). This function adds large amounts of lines to a csv object where each element contains a format string. The vulnerability is not based on format string, rather the large amount of input sent to the program, as at least 50 lines will cause the program to segfault. The other vulnerability in csv2 which causes the program to crash, is the case where the program is sent no input

### JSON fuzzing:

The json fuzzer mutates the json string all the while keeping it as valid json input. Strategies include adding and removing fields, flipping bits in random fields, swapping values of random fields (e.g. int to array of strings) and ‘smart swapping’ the field (e.g. int to negative number or MAX_INT + 1). It chooses a random strategy each time, mutates the json input and then passes it into the program. 

### XML fuzzing:

The main approach for XML fuzzing was to mutate all available fields in the given XML document. The fuzzer uses a Python API, ElementTree to parse and decompose the XML document into parts in order to simplify the accessing and modifying of XML elements.

The fuzzing involves two stages:  

1.  Mutating the existing attributes and text within tags
- Attributes and text within tags that can be modified without breaking XML syntax, are replaced randomly with pre-defined ‘FUZZ CONSTANTS’ such as known integers (large positive and negative integers), empty string, large string, format strings, bad URL, and special characters for XML file.

2. Adding predefined DOM elements to the XML structure
- New DOM elements such as \<div>, \<span>, \<a> and \<p> are added into the XML structure. During our testing, we found that adding unnecessary tags and ridiculously large number of attributes would not result in any existing exploits but would adversely impact the time complexity. Therefore, we also explicitly defined a few DOM elements which include 4-5 attributes each, in the hope that it would be enough for the fuzzer to discover a vulnerability while solving the issue mentioned above. 

### Plaintext fuzzing:

For each line of the sample input, we input randomly generated strings that vary in length and type as well as bit flipping random bits in the sample input. By keeping some of the sample input lines that may be valid inputs for the binary we are able to increase visited code paths.

### Harness:

Our harness implements the basic features required for a fuzzer. This includes:
- Detecting “hangs” and loops via the timeout approach
- Additionally our harness detects the code coverage of our own fuzzer , through seeing which mutation strategy it has passed through and detecting what type of input caused the program to crash
- An update log is displayed approximately every 1000 iterations, which displays the total amount of seg faults, types of crashes and code coverage of our own fuzzer. These logging capabilities are implemented inside each respective fuzzer file type.

Improvements
- There is no “learning” system implemented in our fuzzer, rather it is more of a mutation based fuzzer. 
- Ideally we would have liked to iteratively keep mutating fuzzed input, that reaches closer to code coverage
- The choice of python ultimately means slower speeds, to improve this we would have used a more efficient language. 
-Didn't get a chance to implement the code coverage of the binary file; rather we focused on code coverage of our own fuzzer, and how many times it hits each mutation strategy.

