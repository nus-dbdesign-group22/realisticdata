import random

from generator_types.base import BaseTypeGenerator


class Email(BaseTypeGenerator):
    email_providers = ["@gmail.com",
                       "@yahoo.com",
                       "@outlook.com",
                       "@aol.com",
                       "@protonmall.com",
                       "@icloud.com",
                       "@gmx.com"]

    def get_next_value(self, related_values=None) -> any:
        sample = ""
        if related_values:
            firstname = related_values[0].lower()
            lastname = related_values[1].lower()
            sample = firstname + lastname + random.choice(self.email_providers)
        return sample
