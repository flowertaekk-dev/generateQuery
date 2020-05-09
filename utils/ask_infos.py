#!/usr/bin/python3

from pathlib import Path
from codeDef import *

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
