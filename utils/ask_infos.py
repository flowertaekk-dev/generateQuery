#!/usr/bin/python3

from pathlib import Path
from codeDef import *
from utils.validation import does_the_same_file_name_exist
from utils.messages import messages

############################################
######## retrieve command arguments ########
############################################

# return command argument
def get_arguments(args):
    input_file, output_file = None, None

    if not len(args):
        return None

    if args[1] == '--help':
        print(messages.get(args[1]))
        exit()

    input_file_index = args.index('-i') if '-i' in args else None
    output_file_index = args.index('-o') if '-o' in args else None

    try:
        if input_file_index is not None:
            input_file = args[input_file_index + 1]

        if output_file_index is not None:
            output_file = args[output_file_index + 1]
            does_the_same_file_name_exist(output_file)

        return (input_file, output_file)

    except IndexError as ex:
        print('argument error: ', ex)
        exit()

    return None


############################################
############# ask information ##############
############################################

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
    
    # Check if the same file name exists
    does_the_same_file_name_exist(file_name)

    return file_name

# ask what kind of database is being used
def get_database():
    print('Enter the target database : ', end='')
    db = input()

    if not db in database.keys():
        print('Sorry. {0} is unregistered database.'.format(db))
        exit()
    
    return database.get(db)
