import random

from generator_types.base import BaseTypeGenerator


class String(BaseTypeGenerator):
    def get_next_value(self, related_values=None) -> any:
        options = self.options
        sample = ""
        # if has ref dependence, choose from list of ref values
        # if has FD dependence, check if has already generated, else 
        # need to know current index
        # if have none of those, generate normally
        if "values" in options.keys():
            values = list(options["values"].split(","))
            sample = random.choice(values).replace("_", " ")
        return sample
