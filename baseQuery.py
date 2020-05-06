#!/usr/bin/python3

import re

# TODO need to get file name from user
def getInputFile():
    pass

def getOutputFileName():
    pass

# Read file
def readFile(file_name):
    with open('query.txt', 'r', encoding='utf8') as input_source: # TODO need to use argument
        input_query = ''

        while True:
            line = input_source.readline()
            if not line:
                break;

            #  TODO add validation
                # does it start with unexpected character?
                # TODO will it acceptable not to have comma at the end of the line?
            if re.match('^[-]{2,}', line):
                continue # ignore comment

            input_query += line

    return input_query

# Write file
def writeQuery(output_file):
    with open('output.txt', 'w', encoding='utf8') as output_source:
        pass



#####################################################################
################################# LOGIC #############################
#####################################################################

input_file = getInputFile()
output_file = getOutputFileName()

query = readFile(input_file)
print(query)

# writeQuery(output_file)