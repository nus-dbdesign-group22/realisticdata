from __future__ import annotations
from generator_types.base import BaseTypeGenerator
from generator_types.stringtype import String
from generator_types.number import Number
from generator_types.id import Id
from generator_types.height import Height
from generator_types.weight import Weight

COLUMN_DATATYPES: dict[str, BaseTypeGenerator] = {
    "string": String,
    "number": Number, 
    "id": Id,
    "first_name": BaseTypeGenerator, 
    "last_name": BaseTypeGenerator, 
    "email": BaseTypeGenerator, 
    "text": BaseTypeGenerator, 
    "date": BaseTypeGenerator, 
    "time": BaseTypeGenerator,
    "height": Height,
    "weight": Weight,
}


class JointDependency:
    dependants = []

    def __init__(self, dependants: list[str]):
        self.dependants = dependants

    def get_joint_dependants(self, column_type: str):
        joint_dependants = self.dependants.copy()
        joint_dependants.remove(column_type)
        return joint_dependants


class GeneratorSettings:
    tables: dict[str, Table] = {}
    references: list[Reference] = []
    dependencies: list[Dependency] = []
    joint_dependencies: list[JointDependency] = [JointDependency(["height", "weight"])]

class Column:
    def __init__(self, name: str, datatype: str):
        if datatype not in COLUMN_DATATYPES.keys():
            raise Exception("column type " + datatype + " invalid")
        self.name: str = name
        self.datatype: str = datatype
        self.table_name: str = ""
        self.options: dict[str, str] = {}
        self.generator: BaseTypeGenerator = COLUMN_DATATYPES[datatype](self.options)
        self.generation_priority: int = 0 # to be used by the generator
        self.generated: list[any] = []

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
        self.columns: dict[str, Column] = {}
        self.columns_ordering: list[str] = []
    
    def add_column(self, column: Column):
        column.table_name = self.name
        self.columns[column.name]= column
        self.columns_ordering.append(column.name)


# QualifiedColumnName is a representation of a column in a table 
# with the format {table_name}.{column_name}
class FullColumnName:
    def __init__(self, longname: str):
        table_name, column_name = longname.split(".")
        self.table: str = table_name
        self.column: str = column_name

    def __repr__(self):
        return self.table + "." + self.column
    
    def __eq__(self, other):
        if isinstance(other, FullColumnName):
            return self.table == other.table and self.column == other.column
        return False

    def __hash__(self):
        return hash(self.table+self.column)

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
