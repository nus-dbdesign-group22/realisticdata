from datatypes import GeneratorSettings

class Generator:
    def __init__(self, settings: GeneratorSettings):
        self.settings = settings

    def generate(self):
        print("im generating the data based on this settings:", self.settings)