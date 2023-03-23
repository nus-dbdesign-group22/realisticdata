#!/usr/bin/python3
import os
import sys
import getopt
import time

import pandas as pd
import re

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
        line = file.readline()
        tables = {}
        while line:
            # Remove indentation, whitespaces, etc.
            line = line.strip()
            # Ignore comments
            if len(line) == 0:
                pass
            elif line.startswith("#"):
                pass
            elif line.startswith("CREATE TABLE"):
                create_table(file, line, tables)
            line = file.readline()

    with open('results.txt', 'w') as results:
        results.write("We are currently working on this part...\n")
        results.write("\n")
        results.write("Welcome back later :)")


def create_table(file, line, tables):
    """
    Iterates through the text file until the end of the CREATE TABLE statement is found, while building the table.
    :param file:    The current text file
    :param line:    The current line
    :param tables:  A dictionary with all the tables, with the table name as key
    :return:        Updates the tables dictionary
    """
    statement = line.split(" ")
    df = pd.DataFrame(index = ['0'])
    while True:
        line = file.readline()
        statement.extend(re.split("\W+", str(line)))
        if ");" in str(line):
            break
    for i in reversed(range(len(statement))):
        if statement[i] in "(),;. ":
            statement.pop(i)
    i = 0
    foreign_keys = []
    while i < len(statement):
        if statement[i] == "CREATE":
            try:
                if statement[i + 1] == "TABLE":
                    print("Creating table", statement[i + 2], "...")
                    tables[statement[i + 2]] = df
                    i += 3
                    while statement[i] != "PRIMARY" and statement[i] != "FOREIGN":
                        df[statement[i]] = statement[i + 1]
                        i += 2
                else:
                    raise Exception("CREATE TABLE formatted incorrectly")
            except IndexError:
                raise Exception("CREATE TABLE formatted incorrectly")
        elif statement[i] == "PRIMARY":
            try:
                if statement[i + 1] == "KEY":
                    offset = 2
                    keys = []
                    while i + offset < len(statement):
                        if statement[i + offset] == "FOREIGN":
                            break
                        keys.append(statement[i + offset])
                        offset += 1
                    df["PRIMARY_KEY"] = [keys]
                    i += offset
                else:
                    raise Exception("CREATE TABLE formatted incorrectly")
            except IndexError:
                raise Exception("CREATE TABLE formatted incorrectly")
        elif statement[i] == "FOREIGN":
            try:
                if statement[i + 1] == "KEY":
                    offset = 2
                    ref_offset = offset + 1
                    while statement[i + ref_offset] != "REFERENCES":
                        ref_offset += 1
                    ref_offset += 1
                    n_keys = ref_offset - offset - 1
                    for k in range(n_keys):
                        # Append [attribute_name, foreign table, foreign attribute_name]
                        foreign_keys.append([statement[i + offset + k],
                                            statement[i + ref_offset],
                                            statement[i + ref_offset + k + 1]])
                    df['FOREIGN_KEYS'] = [foreign_keys]
                    i += ref_offset + n_keys
                else:
                    raise Exception("CREATE TABLE formatted incorrectly")
            except IndexError:
                raise Exception("CREATE TABLE formatted incorrectly")
        else:
            i += 1
    print(df)


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
