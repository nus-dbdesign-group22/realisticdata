from __future__ import annotations
import random
from generator_types.base import BaseTypeGenerator


class Date(BaseTypeGenerator):

    def get_range_option(self) -> tuple[int, int]:
        raw_str = self.options["range"]
        delim = raw_str.index("..")
        min_str = raw_str[:delim]
        max_str = raw_str[delim + 2:]
        min = int(min_str)
        max = int(max_str)
        return min, max

    def get_next_value(self, related_values=None) -> any:
        if "range" in self.options.keys():
            min_value, max_value = self.get_range_option()
            year = random.randint(min_value, max_value)
        else:
            year = random.randint(1943, 2010)
        month = random.randint(1, 12)
        if year % 4 == 0 and month == 2:
            day = random.randint(1, 29)
        elif month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        else:
            day = random.randint(1, 30)
        return str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)