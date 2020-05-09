#!/usr/bin/python3

#################################
########### Validation ##########
#################################

# check if written type is in support (if not, we can add it)
def does_type_exist(line_without_space, data_type):
    return line_without_space.split(' ')[0] == data_type