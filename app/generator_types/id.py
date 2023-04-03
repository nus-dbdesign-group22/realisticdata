import random
from generator_types.base import BaseTypeGenerator

class Id(BaseTypeGenerator):
    counter = 1
    """
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
    """

    def get_next_value(self, related_values=None) -> any:
        self.counter += 1
        return self.counter - 1
