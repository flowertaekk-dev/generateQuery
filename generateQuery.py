#!/usr/bin/python3

import re
import sys
from codeDef import *
from utils import *
from domain.column_definition import Column
    
#####################################################################
############################## Read file ############################
#####################################################################

def read_file(file_name):

    if file_name is None:
       file_name = ask_infos.get_input_file_name()

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

#####################################################################
############################# Write file ############################
#####################################################################

def write_query(query, output_file):

    if output_file is None:
        output_file = ask_infos.get_output_file_name()

    with open(output_file, 'w', encoding='utf8') as output_source:
        result_query = ''

        db = ask_infos.get_database()

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

                    column = Column(line_without_space, db)

                    '''
                        Check if it is the last line.
                        If it is the last line, add ');' at the end of the line instead of comma
                    '''
                    if util.isLastLine(split_to_lines_by_LF, i):
                        result_query += util.generateQuery(True, column)
                    else:
                        result_query += util.generateQuery(False, column)

            else:
                output_source.write(result_query)

        except ValueError as err:
            print(err)
        

#####################################################################
################################# LOGIC #############################
#####################################################################

(input_file, output_file) = ask_infos.get_arguments(sys.argv)

# retrieve query
query = read_file(input_file)

# write query
write_query(query, output_file)
