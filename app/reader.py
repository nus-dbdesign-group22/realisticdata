import argparse
import pandas as pd
import re

from datatypes import GeneratorSettings, Table, Column, Dependency, FullColumnName, Reference

class InputReader:
    def __init__(self, input_file, output_file):
        # init variables that was passed in, and their defaults
        self.input_file = ""
        if input_file:
            self.input_file = input_file
        self.output_file = ""
        if output_file:
            self.output_file = output_file
        self.output_format = "csv"
        # init other internal class variables
        self.file = self.line = None
        self.lineNum = 1
        self.current_section = ""
        self.parsedInput = GeneratorSettings()
    
    def read_column_option(self, raw_option: str, column: Column) -> Column:
        splitted = raw_option.split("=")
        option_name = splitted[0]
        option_value = ""
        if len(splitted) > 1:
            option_value = splitted[1]
        column.set_option(option_name, option_value)
        return column

    def read_table_schema(self):
        words = self.line.split(" ")

        # extract table name
        table_name = words[1]
        # extract amount
        amount = 10
        for word in words:
            if word.startswith("amount="):
                amount_str = word.split("=")[1]
                if len(amount_str) > 0:
                    amount = int(amount_str)
        
        newTable = Table(table_name, amount)

        # read the columns
        self.line = self.file.readline()
        self.lineNum += 1
        while True:
            self.line = self.line.strip()
            if self.line == ")":
                break
            words = self.line.split(" ")

            # guard check
            if len(words) < 2:
                raise Exception("invalid column declaration at " + str(self.lineNum))

            # read name and type
            column_name = words[0]
            column_type = words[1]
            newColumn = Column(column_name, column_type)

            # read all options
            words = words[2:]
            for word in words:
                self.read_column_option(word, newColumn)

            # finish processing a column
            newTable.add_column(newColumn)
            self.line = self.file.readline()
            self.lineNum += 1

        self.parsedInput.tables[table_name] = newTable

    def read_table_dependencies(self):
        words = self.line.split(" ")

        # extract table name
        table_name = words[1]

        # read the dependencies in table
        self.line = self.file.readline()
        self.lineNum += 1
        while True:
            self.line = self.line.strip()
            if self.line == ")":
                break
            words = self.line.split(" ")

            # guard check
            if len(words) < 3:
                raise Exception("invalid dependency declaration at " + str(self.lineNum))

            # locate the arrow "->" and LHS and RHS
            arrow_index = words.index("->")
            LHS_str = words[:arrow_index]
            RHS_str = words[arrow_index+1:]

            # turn each item in LHS and RHS to FullColumnName
            LHS: list[FullColumnName] = []
            for column_name in LHS_str:
                LHS.append(FullColumnName(table_name + "." + column_name))
            RHS: list[FullColumnName] = []
            for column_name in RHS_str:
                RHS.append(FullColumnName(table_name + "." + column_name))
            newDependency = Dependency(LHS, RHS)

            # finish processing a dependency
            self.parsedInput.dependencies.append(newDependency)
            self.line = self.file.readline()
            self.lineNum += 1

    def read_standalone_reference(self): 
        self.line = self.line.strip()
        words = self.line.split(" ")

        # guard check
        if len(words) != 4:
            raise Exception("invalid reference declaration at " + str(self.lineNum))

        # remove the first element "reference:"
        words = words[1:]

        column1 = FullColumnName(words[0])
        column2 = FullColumnName(words[2])
        new_reference = Reference(column1, column2, words[1])
        self.parsedInput.references.append(new_reference)

    def read_standalone_dependency(self):
        self.line = self.line.strip()
        words = self.line.split(" ")

        # guard check
        if len(words) < 3:
            raise Exception("invalid dependency declaration at " + str(self.lineNum))

        # locate the arrow "->" and LHS and RHS
        arrow_index = words.index("->")
        LHS_str = words[:arrow_index]
        RHS_str = words[arrow_index+1:]

        # turn each item in LHS and RHS to FullColumnName
        LHS: list[FullColumnName] = []
        for column_name in LHS_str:
            LHS.append(FullColumnName(column_name))
        RHS: list[FullColumnName] = []
        for column_name in RHS_str:
            RHS.append(FullColumnName(column_name))
        newDependency = Dependency(LHS, RHS)

        # finish processing a dependency
        self.parsedInput.dependencies.append(newDependency)

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
                    self.read_standalone_dependency()
                
                self.lineNum = self.lineNum +1
                self.line = self.file.readline()
        
        return self.parsedInput
