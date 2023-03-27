import argparse
import pandas as pd
import re

def readfile(input_file):
    """
    Function that reads the input from the user.

    :param input_directory: Directory with the input file
    :param input_file:      File with the ER Design, formatted as specified
    :return                 Write a results.txt file with the result to input_directory
    """

    with open(input_file, 'r') as file:
        line = file.readline()
        tables = {}
        n_rows = 10
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
        add_rows(tables, n_rows)
        for key in tables.keys():
            print(tables[key])

    with open('results.txt', 'w') as results:
        results.write("We are currently working on this part...\n")
        results.write("\n")
        results.write("Welcome back later :)")


def add_rows(tables, n):
    for key in tables.keys():
        df = tables[key]
        columns = list(df.columns)
        try:
            columns.remove("PRIMARY_KEY")
        except ValueError:
            pass
        try:
            columns.remove("FOREIGN_KEYS")
        except ValueError:
            pass
        for i in range(n):
            data = []
            for j in range(len(columns)):
                data.append(chr(97 + j) + str(i + 1))
            df = pd.concat([df, pd.DataFrame([data], columns=columns, index=[i+1])])
        tables[key] = df


def create_table(file, line, tables):
    """
    Iterates through the text file until the end of the CREATE TABLE statement is found, while building the table.
    :param file:    The current text file
    :param line:    The current line
    :param tables:  A dictionary with all the tables, with the table name as key
    :return:        Updates the tables dictionary
    """
    statement = line.split(" ")
    df = pd.DataFrame(index=['0'])
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

def readinput():
    parser = argparse.ArgumentParser(
        description='generate realistic mock data based on complex user inputs',
    )

    parser.add_argument('-i', '--input', help='path to the input file', required=True)
    parser.add_argument('-o', '--output', help='(optional) path to the output file. If not specified will print to stdout')
    parser.add_argument('-f', '--format', help='(optional) output format -- options are: csv, sql. Default is csv (feature is WIP)')
    args = parser.parse_args()

    input_file = args.input

    readfile(input_file)
