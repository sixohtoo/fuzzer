from pwn import *
import json
def runner(binary, input_text, lock):
	# Lock used later when multithreading is implemented

	p = process(binary)

	# These 4 lines were for testing we will need to delete them
	input_text.seek(0) # Make sure you seek to 0 - loading the file in the input check moves the file handle
	contents = input_text.read().strip()
	log = json.loads(contents)
	print(log)


	p.sendline(contents) # Change this to input_text

	exit_code = None

	while exit_code is None:
		exit_code = p.poll()
	p.close()

	if(exit_code != 0):
		bad = open('bad.txt', 'w')
		bad.write(input_text + ' caused ' + exit_code)
		bad.close()
	return # Something (maybe True/False depending on whether than input found a crash?)
