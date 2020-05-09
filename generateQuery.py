#!/usr/bin/python3

import re
from pathlib import Path

from codeDef import *

#####################################################################
################################# UTIL ##############################
#####################################################################

#################################
########## filter data ##########
#################################

# retrieve column name in a line
def retrieve_column_name(query):
    column_name = re.split('[\s]', query)[1] # get column name only
    return column_name.replace(',', '') # remove comma if exists

# retrieve constraint in a line
def retrieve_constraint(query):
    constraint = ''
    for cons in constraints:
        if cons in query:
            constraint = ' ' + cons # add space to give space after data_type
            break
    return constraint

#################################
######## ask information ########
#################################

# ask query tempate file name
def get_input_file_name():
    print('Enter input file name : ', end='')
    file_name = input()

    # File not found!
    path = Path(file_name)
    if not path.is_file():
        raise FileNotFoundError

    return file_name

# ask output file name
def get_output_file_name():
    print('Enter output file name : ', end='')
    file_name = input()
    
    # check if exists?
    path = Path(file_name)
    if path.is_file():
        # ask once more if they are sure to overwrite
        print('The existing file will be overwritten. Are you sure of doing it?\n(y/n)', end='')
        overwrite = input()

        if overwrite == 'y':
            pass
        elif overwrite == 'n':
            file_name = get_output_file_name()
        else:
            print('Unexpected character : {0}'.format(overwrite))
            exit()

    return file_name

# ask what kind of database is being used
def get_database():
    print('Enter the target database : ', end='')
    db = input()

    if not db in database.keys():
        print('Sorry. {0} is unregistered database.'.format(db))
        exit()
    
    return database.get(db)

#################################
########### Validation ##########
#################################

# check if written type is in support (if not, we can add it)
def does_type_exist(line_without_space, data_type):
    return line_without_space.split(' ')[0] == data_type

#################################
############# Common ############
#################################

# check if it is the last query line
def isLastLine(split_to_lines_by_LF, index):
    return re.match('^\);', split_to_lines_by_LF[index + 1])

# translate template to query line by line
def generateQuery(isLastLine: bool, query_line: str, data_type: str, constraint=''):
    line = '\t{column} {data_type}{constraint}\n);' if isLastLine else '\t{column} {data_type}{constraint},\n'

    return line.format(column=retrieve_column_name(query_line), data_type=data_type, constraint=constraint)
    
#####################################################################
############################ CORE FUNCTION ##########################
#####################################################################

#################################
########### Read file ###########
#################################

def read_file(file_name):
    with open(file_name, 'r', encoding='utf8') as input_source:
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

#################################
########### Write file ##########
#################################

def write_query(query, output_file):
    with open(output_file, 'w', encoding='utf8') as output_source:
        result_query = ''

        db = get_database()

        try:
            split_to_lines_by_LF = query.split('\n')

            for i, line in enumerate(split_to_lines_by_LF, start=0):
                line_without_space = line.strip()

                # skip empty line
                if line_without_space == '':
                    continue

                # check if it is create statement
                if line_without_space.startswith('CREATE'):
                    result_query += '{0}\n'.format(line_without_space)
                    continue

                # check query format
                if re.match('^[A-Z]{1,2}\s[0-9a-zA-Z]*', line_without_space):

                    # check unexpected character
                    '''
                        It(db.key) should be single character otherwise certain character has already been used.
                        ex)
                            Let's say we define like:
                                B - BOOLEAN (O)
                            Next, we want to add new definition like:
                                B - BLOB (X)
                            But, 'B' has already been used. Therefore, we need to find out other way to express it like:
                                BL - BLOB (O)
                        So, we can avoid Vaildation error even if it is actually 'BL' since 'B' must have been defined.

                        NOT SURE IT IS THE BEST WAY.
                    '''
                    if not line_without_space[0] in db.keys():
                        raise ValueError('Invalid format : {0}'.format(line_without_space))

                    # create query
                    for code_def, code_type in db.items():
                        # check if specified data type is supported
                        if (not does_type_exist(line_without_space, code_def)):
                            continue;

                        # check if it has constraint
                        constraint = retrieve_constraint(line_without_space)

                        '''
                            Check if it is the last line.
                            If it is the last line, add ');' at the end of the line instead of comma
                        '''
                        if isLastLine(split_to_lines_by_LF, i):
                            result_query += generateQuery(True, line_without_space, code_type, constraint)
                        else:
                            result_query += generateQuery(False, line_without_space, code_type, constraint)

                        # remove constraint
                        constraint = ''
                        break
            else:
                output_source.write(result_query)

        except ValueError as err:
            print(err)
        

#####################################################################
################################# LOGIC #############################
#####################################################################

input_file = get_input_file_name()
output_file = get_output_file_name()

# retrieve query
query = read_file(input_file)

# write query
write_query(query, output_file)