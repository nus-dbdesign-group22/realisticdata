import random

class BaseTypeGenerator:
    def __init__(self, options: dict[str, str]):
        self.options: dict[str, str] = options
        self.referencing_values: list[any] = [] # for references / relationships
        self.dependent_values: list[list[any]] = [] # for functional dependencies
        self.related_values: list[list[any]] = [] # for any other related columns
        self.generated_dependent_values: dict[any, any] = {}
        self.previously_generated: list[any] = []

    def set_referencing_values(self, referencing_values: list[any]):
        self.referencing_values = referencing_values

    def set_dependent_column(self, dependent_column: list[any]):
        self.dependent_values.append(dependent_column)
    
    def set_related_column(self, related_column: list[any]):
        self.related_values.append(related_column)
    
    def get_related_values(self, index: int) -> list[any]:
        related_values = []
        if len(self.related_values) > 0:
            for i in self.related_values:
                related_values.append(i[index])
        return related_values

    def get_related_values_as_tuple(self, index:int) -> tuple[any]:
        related_values = ()
        if len(self.related_values) > 0:
            for i in self.related_values:
                related_values = related_values + (i[index],)
        return related_values

    def get_next_row(self, current_index: int) -> any:
        # if has ref dependence, choose from list of ref values
        if len(self.referencing_values) > 0:
            return random.choice(self.referencing_values)
        
        # if has FD dependence, check if has already generated, if yes then select that value
        determinants = None
        if len(self.dependent_values) > 0:
            determinants = ()
            for i in self.dependent_values:
                determinants = determinants + (i[current_index],)
            if determinants in self.generated_dependent_values.keys():
                return self.generated_dependent_values[determinants]
            
        value = self.get_next_value()

        if determinants:
            self.generated_dependent_values[determinants] = value

        # if there is a unique flag, generate until we have a unique value
        if "unique" in self.options.keys() and self.options["unique"]=="true":
            while True:
                if value not in self.previously_generated:
                    break
                value = self.get_next_value()
            self.previously_generated.append(value)
        
        return value

    def get_next_value(self) -> any:
        pass