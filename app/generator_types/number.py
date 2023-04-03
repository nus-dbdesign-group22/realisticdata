import random
from generator_types.base import BaseTypeGenerator

class Number(BaseTypeGenerator):
    def get_range_option(self) -> tuple[int, int]:
        raw_str = self.options["range"]
        delim = raw_str.index("..")
        min_str = raw_str[:delim]
        max_str = raw_str[delim+2:]
        min = 0
        max = 1000
        if len(min_str) > 0:
            min = int(min_str)
        if len(max_str) > 0:
            max = int(max_str)
        return min, max
    
    def random_decimal(self, min_value: int, max_value: int):
        decimal_places = 3
        if "decimal_places" in self.options.keys():
            decimal_places = int(self.options["decimal_places"])
        return round(random.uniform(min_value, max_value), decimal_places)

    def get_next_value(self, related_values=None) -> any:
        min_value = 0
        max_value = 1000
        if "range" in self.options.keys():
            min_value, max_value = self.get_range_option()
        if "decimal" in self.options.keys():
            return self.random_decimal(min_value, max_value)
        return random.randint(min_value, max_value)