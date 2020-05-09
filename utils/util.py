#!/usr/bin/python3

import re
from utils import filters

#################################
############# Common ############
#################################

# check if it is the last query line
def isLastLine(split_to_lines_by_LF, index):
    return re.match('^\);', split_to_lines_by_LF[index + 1])

# translate template to query line by line
def generateQuery(isLastLine: bool, query_line: str, data_type: str, constraint=''):
    line = '\t{column} {data_type}{constraint}\n);' if isLastLine else '\t{column} {data_type}{constraint},\n'

    return line.format(column=filters.retrieve_column_name(query_line), data_type=data_type, constraint=constraint)