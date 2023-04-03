from datatypes import Column, GeneratorSettings, Reference, FullColumnName, BaseTypeGenerator
import os
import csv
class Generator:
    def __init__(self, settings: GeneratorSettings):
        self.settings = settings
        self.calculated_order: dict[FullColumnName, bool] = {}
        self.order_of_generation: list[list[FullColumnName]] = []

    def preprocess_reference(self):
        # step 1: convert all reference declared in column options into standalone reference objects
        for _, table in self.settings.tables.items():
            for _, column in table.columns.items():
                column1 = column.get_name()
                for option, value in column.options.items():
                    if option == "reference":
                        relationship = value[0]
                        column2_str = value[1:]
                        if value.startswith("<>"):
                            relationship = "<>"
                            column2_str = value[2:]
                        newReference = Reference(column1, FullColumnName(column2_str), relationship)
                        self.settings.references.append(newReference)

        # step 2: go through all references and add unique constraint to all 
        # "one" side in all "one-to-many" and "many-to-one" relationships
        # additionally, let the column's generator know of the other column's values so it can reference them
        for reference in self.settings.references:
            if reference.relationship == "<" or reference.relationship == "~":
                self.settings.tables[reference.column1.table].columns[reference.column1.column].options["unique"]="true"
                self.settings.tables[reference.column2.table].columns[reference.column2.column].generator.set_referencing_values(
                    self.settings.tables[reference.column1.table].columns[reference.column1.column].generated
                )
            if reference.relationship == ">" or reference.relationship == "~":
                self.settings.tables[reference.column2.table].columns[reference.column2.column].options["unique"]="true"
                self.settings.tables[reference.column1.table].columns[reference.column1.column].generator.set_referencing_values(
                    self.settings.tables[reference.column2.table].columns[reference.column2.column].generated
                )
            if reference.relationship == "<>":
                self.settings.tables[reference.column1.table].columns[reference.column1.column].generator.set_referencing_values(
                    self.settings.tables[reference.column2.table].columns[reference.column2.column].generated
                )
                self.settings.tables[reference.column2.table].columns[reference.column2.column].generator.set_referencing_values(
                    self.settings.tables[reference.column1.table].columns[reference.column1.column].generated
                )
    
    def preprocess_primary_key(self):
        # add unique constraint to all primary key
        # TODO: Deal with situation where composite primary key
        for _, table in self.settings.tables.items():
            for _, column in table.columns.items():
                if "primary_key" in column.options.keys() and "unique" not in column.options.keys():
                    column.options["unique"]="true"

    def recursive_calculate_order(self, column_name: FullColumnName) -> int:
        # build a list of dependents
        dependents: list[FullColumnName] = []
        for reference in self.settings.references:
            if column_name == reference.column1 and reference.relationship == ">":
                dependents.append(reference.column2)
            if column_name == reference.column2 and reference.relationship == "<":
                dependents.append(reference.column1)
        for dependency in self.settings.dependencies:
            if column_name in dependency.LHS:
                dependents.extend(dependency.RHS)
        # find max
        max_dependent_priority = 0
        for dependent in dependents:
            dependent_priority = self.recursive_calculate_order(dependent)
            if dependent_priority > max_dependent_priority:
                max_dependent_priority = dependent_priority
        # if current prio <= max prio, set, otherwise leave it as it is
        current_column = self.settings.tables[column_name.table].columns[column_name.column]
        if current_column.generation_priority <= max_dependent_priority:
            current_column.generation_priority = max_dependent_priority + 1
        self.calculated_order[column_name] = True
        return current_column.generation_priority
    
    def preprocess_calculate_order(self):
        # first, ALL primary keys gets to generate first
        for _, table in self.settings.tables.items():
            for _, column in table.columns.items():
                if "primary_key" in column.options.keys():
                    column.generation_priority += 1

        # iterate through all references
        for reference in self.settings.references:
            if reference.relationship == "<" and not self.calculated_order.get(reference.column1, False):
                self.recursive_calculate_order(reference.column1)
            if reference.relationship == ">" and not self.calculated_order.get(reference.column2, False):
                self.recursive_calculate_order(reference.column2)
        
        # iterate through all dependencies
        for dependency in self.settings.dependencies:
            for column_name in dependency.LHS:
                if not self.calculated_order.get(column_name, False):
                    self.recursive_calculate_order(column_name)

        # build a list representing the order of generation
        for _, table in self.settings.tables.items():
            for _, column in table.columns.items():
                while len(self.order_of_generation) <= column.generation_priority:
                    self.order_of_generation.append([])
                self.order_of_generation[column.generation_priority].append(column.get_name())
        # now reverse it
        self.order_of_generation.reverse()
    
    def prepare_generator(self, column: Column):
        # let the generator know of the FD columns
        for dependency in self.settings.dependencies:
            if column.get_name() in dependency.RHS:
                for LHS_column_name in dependency.LHS:
                    LHS_column = self.settings.tables[LHS_column_name.table].columns[LHS_column_name.column]
                    column.generator.set_dependent_column(LHS_column.generated)
        # let the generator know of the related columns
        for _, table in self.settings.tables.items():
            for _, column in table.columns.items():
                if "related" in column.options.keys():
                    columns = column.options["related"].split(",")
                    for c in columns:
                        related_column = FullColumnName(c)
                        related_column_values = self.settings.tables[related_column.table].columns[related_column.column].generated
                        column.generator.set_related_column(related_column_values)
    
    def print_result(self):
        for _, table in self.settings.tables.items():
            print("table: " + table.name + ":")
            row=""
            for column_name in table.columns_ordering:
                row=row+column_name+"\t"
            print(row)
            for i in range(table.amount):
                row=""
                for column_name in table.columns_ordering:
                    row=row+str(table.columns[column_name].generated[i])+"\t"
                print(row)
            print("-----")

    def generate_output(self, output_directory):
        os.chdir(output_directory)
        for _, table in self.settings.tables.items():
            with open(table.name + ".csv", "w", newline='') as file:
                writer = csv.writer(file)
                first_row = []
                for column_name in table.columns_ordering:
                    first_row.append(column_name)
                writer.writerow(first_row)
                for i in range(table.amount):
                    row = []
                    for column_name in table.columns_ordering:
                        row.append(table.columns[column_name].generated[i])
                    writer.writerow(row)


    def generate(self, output_directory=None):
        # pre-processing and data preparation steps
        self.preprocess_reference()
        self.preprocess_primary_key()
        self.preprocess_calculate_order()

        # start actually generating
        for list_of_columns in self.order_of_generation:
            for column_name in list_of_columns:
                table = self.settings.tables[column_name.table]
                column = table.columns[column_name.column]
                self.prepare_generator(column)
                for i in range(table.amount):
                    column.generated.append(column.generator.get_next_row(i))

        # print the result (output WIP)
        self.print_result()
        if output_directory:
            self.generate_output(output_directory)