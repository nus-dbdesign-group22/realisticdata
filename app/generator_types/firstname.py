from generator_types.base import BaseTypeGenerator
import names


class FirstName(BaseTypeGenerator):

    def get_next_value(self, related_values=None) -> any:
        sample = names.get_first_name()
        return sample
