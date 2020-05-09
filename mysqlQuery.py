#!/usr/bin/python3

import re
from codeDef import mysql_def, constraints

#####################################################################
################################# UTIL ##############################
#####################################################################

def retrieveColumnName(query):
    column_name = re.split('[\s]', query)[1] # get column name only
    return column_name.replace(',', '') # remove comma if exists

LF = '\n'
TAB = '\t'

#####################################################################
############################ CORE FUNCTION ##########################
#####################################################################

# TODO need to get file name from user
def getInputFile():
    pass

def getOutputFileName():
    pass

# ask what kind of database is being used
def getDatabase():
    pass

# Read file
def readFile(file_name):
    with open('query.txt', 'r', encoding='utf8') as input_source: # TODO need to use argument
        input_query = ''

        while True:
            line = input_source.readline()
            if not line:
                break

            # ignore comment
            if re.match('^[-]{2,}', line):
                continue
            
            # ignore empty line
            if line == '\n':
                continue

            input_query += line

    return input_query

# Write file
def writeQuery(query, output_file):
    with open('output.txt', 'w', encoding='utf8') as output_source:
        # better to ask file name if it exists

        result = ''

        try:
            split_to_lines = query.split('\n')

            for i, line in enumerate(split_to_lines, start=0):
                line_without_space = line.strip()

                # skip empty line
                if line_without_space == '':
                    continue

                # check if it is create statement
                if line_without_space.startswith('CREATE'):
                    result += '{0}{1}'.format(line_without_space, LF)
                    continue

                # check query format
                if re.match('^[A-Z]{1,2}\s[0-9a-zA-Z]*', line_without_space):
                    # check unexpected character
                    if not line_without_space[0] in mysql_def.keys():
                        raise ValueError('Invalid format : {0}'.format(line_without_space))

                    # create query
                    ## TODO need to convert also constraints
                    for code_def, code_type in mysql_def.items():
                        if (line_without_space.split(' ')[0] == code_def): # need refactoring

                            # need refactoring
                            if re.match('^\);', split_to_lines[i + 1]):
                                result += '{tab}{column} {data_type}{LF});'\
                                    .format(tab=TAB, column=retrieveColumnName(line_without_space), data_type=code_type, LF=LF)
                                break


                            # check if it has constraint
                            for cons in constraints:
                                if cons in line_without_space:
                                    constraint = cons
                                    break

                            result += '{tab}{column} {data_type} {constraint},{LF}'\
                                .format(tab=TAB, column=retrieveColumnName(line_without_space), data_type=code_type, constraint=constraint, LF=LF)

                            # remove constraint
                            constraint = ''
                            break
            else:
                output_source.write(result)

        except ValueError as err:
            print(err)
        

#####################################################################
################################# LOGIC #############################
#####################################################################

input_file = getInputFile()
output_file = getOutputFileName()

# retrieve query
query = readFile(input_file)

# write query
writeQuery(query, output_file)