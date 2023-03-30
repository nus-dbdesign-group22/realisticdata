from __future__ import annotations

COLUMN_DATATYPES = [
    "string",
    "number", 
    "id", 
    "first_name", 
    "last_name", 
    "email", 
    "text", 
    "date", 
    "time",
]

class GeneratorSettings:
    tables: list[Table] = []
    references: list[Reference] = []
    dependencies: list[Dependency] = []

class Column:
    table_name = ""

    def __init__(self, name: str, datatype: str):
        if datatype not in COLUMN_DATATYPES:
            raise Exception("column type " + datatype + " invalid")
        self.name = name
        self.datatype = datatype
        self.options = {}

    def set_option(self, option: str, value: str):
        # TODO validate option before adding it
        self.options[option] = value

    def get_name(self):
        return FullColumnName(self.table_name + "." + self.name)
    
    def __repr__(self):
        return self.get_name()

class Table:
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount
        self.primary_key = None
        self.columns = []
    
    def add_column(self, column: Column):
        column.table_name = self.name
        self.columns.append(column)


# QualifiedColumnName is a representation of a column in a table 
# with the format {table_name}.{column_name}
class FullColumnName:
    def __init__(self, longname):
        table_name, column_name = longname.split(".")
        self.table = table_name
        self.column = column_name

    def __repr__(self):
        return self.table + "." + self.column

class Reference:
    def __init__(self, column1: FullColumnName, column2: FullColumnName, relationship: str):
        self.column1 = column1
        self.column2 = column2
        if not relationship:
            relationship = "<>"
        self.relationship = relationship

class Dependency:
    LHS = []
    RHS = []

    def __init__(self, LHS: list[FullColumnName], RHS: list[FullColumnName]):
        self.LHS = LHS
        self.RHS = RHS
