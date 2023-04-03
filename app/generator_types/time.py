import random
from generator_types.base import BaseTypeGenerator


class Time(BaseTypeGenerator):

    def get_next_value(self, related_values=None) -> any:
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)