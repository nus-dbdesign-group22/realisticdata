import random
from generator_types.base import BaseTypeGenerator


class Date(BaseTypeGenerator):

    def get_next_value(self, related_values=None) -> any:
        year = random.randint(1933, 2020)
        month = random.randint(1, 12)
        if year % 4 == 0 and month == 2:
            day = random.randint(1, 29)
        elif month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        else:
            day = random.randint(1, 30)
        return str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)