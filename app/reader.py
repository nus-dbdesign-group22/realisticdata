import argparse
import pandas as pd
import re

from datatypes import GeneratorSettings

class InputReader:
    def __init__(self, input_file, output_file, output_format):
        # init variables that was passed in, and their defaults
        self.input_file = ""
        if input_file:
            self.input_file = input_file
        self.output_file = ""
        if output_file:
            self.output_file = output_file
        self.output_format = "csv"
        if output_format:
            self.output_format = output_format
        # init other internal class variables
        self.file = self.line = None
        self.lineNum = 1
        self.current_section = ""
        self.parsedInput = GeneratorSettings()

    def read_table_schema(self):
        # TODO implement function
        pass

    def read_table_dependencies(self):
        # TODO implement function
        pass

    def read_standalone_reference(self): 
        # TODO implement function
        pass

    def read_standalone_dependency(self):
        # TODO implement function
        pass

    def read_input(self) -> GeneratorSettings:
        with open(self.input_file, 'r') as self.file:
            self.line = self.file.readline()
            while self.line:
                # Remove trailing and leading indentation, whitespaces, etc.
                self.line = self.line.strip()

                # Ignore empty lines
                if len(self.line) == 0:
                    pass

                # Ignore comments
                elif self.line.startswith("#"):
                    pass

                # reading section declarations
                elif self.line == "section:schema":
                    current_section = "schema"
                elif self.line == "section:dependencies":
                    current_section = "dependencies"

                # reading in table statements
                elif self.line.startswith("table"):
                    if current_section == "schema":
                        self.read_table_schema()
                    elif current_section == "dependencies":
                        self.read_table_dependencies()

                # reading in standalone reference statements
                elif self.line.startswith("reference:"):
                    if current_section == "schema":
                        self.read_standalone_reference()
                    elif current_section == "dependencies":
                        raise Exception("Invalid dependency declaration at line " + str(self.lineNum))

                # reading in standalone dependency statements
                else:
                    if current_section != "dependencies":
                        raise Exception("Invalid input at line " + str(self.lineNum))
                    success = self.read_standalone_dependency()
                    if not success:
                        raise Exception("Invalid input at line " + str(self.lineNum))
                
                self.lineNum = self.lineNum +1
                self.line = self.file.readline()
        
        return 

# old function to read and generate columns
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

# old function to read and generate tables
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

