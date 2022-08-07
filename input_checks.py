import json
import xml
import csv

def check_json(input_text):
	try:
		contents = input_text.read().strip()

		json.loads(contents)
	except:
		print('Input file is NOT a json file')
		return False

	return True
	
def check_xml(input_text): # TODO
	return False
	# try:
	# 	return xml.
	# except:
	# 	return False


def check_csv(input_text): # TODO needs to be more robust (thinks xml is csv)
	try:
		return csv.reader(input_text, delimiter=',')
	except:
		print('Input file is NOT a CSV file')
		return False