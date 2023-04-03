from generator_types.base import BaseTypeGenerator
import names


class LastName(BaseTypeGenerator):

    def get_next_value(self, related_values=None) -> any:
        sample = names.get_last_name()
        return sample
