#!/usr/bin/python3

import re
from codeDef import *

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