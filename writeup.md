Fuzzer
=========

### Features

Currently, the fuzzer is able to mutate both json inputs and csv inputs. It uses mutation strategies specific to the input’s data type as well as some general mutation strategies that are applicable for any type of input.

### Csv Fuzzer
The csv fuzzer mutates the sample input based on three different strategies. This includes flipping random bits, randomly inserting format strings and adding large amounts of lines to a csv object. The strategy is then chosen randomly and sent to the program. 

The main vulnerability stemming from the csv1 file is when the fuzzer calls the function addLines(). This function adds large amounts of lines to a csv object where each element contains a format string. The vulnerability is not based on format string, rather the large amount of input sent to the program, as at least 50 lines will cause the program to segfault.  

### JSON fuzzing:
The json fuzzer mutates the json string all the while keeping it as valid json input. Strategies include adding and removing fields, flipping bits in random fields, swapping values of random fields (e.g. int to array of strings) and ‘smart swapping’ the field (e.g. int to negative number or MAX_INT + 1). It chooses a random strategy each time, mutates the json input and then passes it into the program. 

### Design:
The fuzzer works by first detecting which type of input it’s given and then uses multithreading to call the input type’s respective fuzzer function, which mutates the input data, and runs the provided binary, where it passes in the mutated data through stdin. Currently, the methods used for speeding up the fuzzer are multithreading and reading the input data before the multithreading starts. This allows us to only open the input data file once, which avoids a lot of overhead.
