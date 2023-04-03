from generator_types.base import BaseTypeGenerator

class String(BaseTypeGenerator):
    def get_next_value(self, related_values=None) -> any:
        options = self.column.options
        # if has ref dependence, choose from list of ref values
        # if has FD dependence, check if has already generated, else 
            # need to know current index
        # if have none of those, generate normally
        if "unique" in options.keys() and options["unique"]=="true":
            print("yes unique")
        # if unique then remember it
        return "this is a random string"