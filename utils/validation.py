#!/usr/bin/python3

from pathlib import Path

#################################
########### Validation ##########
#################################

# check if written type is in support (if not, we can add it)
def does_type_exist(line_without_space, data_type):
    return line_without_space.split(' ')[0] == data_type

# check if the same file name does exist
def does_the_same_file_name_exist(output_file):
    path = Path(output_file)
    if path.is_file():
        # ask once more if they are sure to overwrite
        print('The existing file will be overwritten. Are you sure of doing it?(y/n) ', end='')
        overwrite = input()

        if overwrite == 'y':
            pass
        elif overwrite == 'n':
            exit()
        else:
            print('Unexpected character : {0}'.format(overwrite))
            exit()