#!/usr/bin/python3
import os
import sys
import getopt

"""
Run the tool from the terminal using the command

python generate_data.py -i input_directory -f input_file

where input_directory is the directory where the input_file is located and the output file will be written
if no input_file is specified, the user is asked if they want to create an example file with correct format...

How should the input be specified? See input_format_example.txt
"""


def usage():
    print("usage: " + sys.argv[0] + " -i input_directory -f input_file")


def read_input(input_directory, input_file):
    """
    Function that reads the input from the user.

    :param input_directory: Directory with the input file
    :param input_file:      File with the ER Design, formatted as specified
    :return                 Write a results.txt file with the result to input_directory
    """
    # Update current directory
    os.chdir(input_directory)

    with open(input_file, 'r') as file:
        for line in file.readlines():
            # Remove indentation, whitespaces, etc.
            line = line.strip()
            # Ignore comments
            if line.startswith("#"):
                continue
            if len(line) == 0:
                continue
            else:
                print(str(line))

    with open('results.txt', 'w') as results:
        results.write("We are currently working on this part...\n")
        results.write("\n")
        results.write("Welcome back later :)")


def set_up():
    input_directory = input_file = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:f:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == '-i':  # input directory
            input_directory = a
        elif o == '-f':
            input_file = a
        else:
            assert False, "unhandled option"

    if input_directory is None:
        usage()
        sys.exit(2)

    if input_file is None:
        # Suggest to create an example file
        pass

    read_input(input_directory, input_file)


# Run the tool
set_up()
