#!/usr/bin/python3

import re
from pathlib import Path

from codeDef import *

#####################################################################
################################# UTIL ##############################
#####################################################################

LF = '\n'
TAB = '\t'

def retrieve_column_name(query):
    column_name = re.split('[\s]', query)[1] # get column name only
    return column_name.replace(',', '') # remove comma if exists

#####################################################################
############################ CORE FUNCTION ##########################
#####################################################################

def get_input_file_name():
    print('Enter input file name : ', end='')
    file_name = input()

    # File not found!
    path = Path(file_name)
    if not path.is_file():
        raise FileNotFoundError

    return file_name

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


# Read file
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

# Write file
def write_query(query, output_file):
    with open(output_file, 'w', encoding='utf8') as output_source:
        result_query = ''

        db = get_database()

        try:
            split_to_lines = query.split('\n')

            for i, line in enumerate(split_to_lines, start=0):
                line_without_space = line.strip()

                # skip empty line
                if line_without_space == '':
                    continue

                # check if it is create statement
                if line_without_space.startswith('CREATE'):
                    result_query += '{0}{1}'.format(line_without_space, LF)
                    continue

                # check query format
                if re.match('^[A-Z]{1,2}\s[0-9a-zA-Z]*', line_without_space):
                    # check unexpected character
                    if not line_without_space[0] in db.keys():
                        raise ValueError('Invalid format : {0}'.format(line_without_space))

                    # create query
                    for code_def, code_type in db.items():
                        if (line_without_space.split(' ')[0] == code_def): # need refactoring

                            # need refactoring
                            if re.match('^\);', split_to_lines[i + 1]):
                                result_query += '{tab}{column} {data_type}{LF});'\
                                    .format(tab=TAB, column=retrieve_column_name(line_without_space), data_type=code_type, LF=LF)
                                break


                            # check if it has constraint
                            for cons in constraints:
                                if cons in line_without_space:
                                    constraint = ' ' + cons # add space to give space from data_type
                                    break

                            result_query += '{tab}{column} {data_type}{constraint},{LF}'\
                                .format(tab=TAB, column=retrieve_column_name(line_without_space), data_type=code_type, constraint=constraint, LF=LF)

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