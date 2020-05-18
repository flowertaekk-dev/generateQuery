#!/usr/bin/python3

import re
from utils import filters
from domain.column_definition import Column

#################################
############# Common ############
#################################

# check if it is the last query line
def isLastLine(split_to_lines_by_LF, index):
    return re.match('^\);', split_to_lines_by_LF[index + 1])

# translate template to query line by line
def generateQuery(isLastLine: bool, column: Column):
    line = '\t{column} {data_type}{constraint} {comment}\n);\n' if isLastLine else '\t{column} {data_type}{constraint}, {comment}\n'

    column_name = column.get_column_name()
    data_type = column.get_data_type()
    constraint = column.get_constraint()
    comment = column.get_comment()

    return line.format(column=column_name, data_type=data_type, constraint=constraint, comment=comment)
