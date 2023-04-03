import numpy as np
from generator_types.base import BaseTypeGenerator


class Color(BaseTypeGenerator):
    colors = ["Alice blue", "Antique white", "Aqua", "Aquamarine", "Azure", "Beige", "Bisque", "Black",
              "Blanched almond", "Blue", "Blue violet", "Brown", "Burlywood", "Cadet blue", "Chartreuse",
              "Chocolate", "Coral", "Cornflower blue", "Cornsilk", "Crimson", "Cyan", "Dark blue",
              "Dark cyan", "Dark goldenrod", "Dark gray", "Dark green", "Dark khaki", "Dark magenta",
              "Dark olive green", "Dark orange", "Dark orchid", "Dark red", "Dark salmon", "Dark seagreen",
              "Dark slate blue", "Dark slate gray", "Dark turquoise", "Dark violet", "Deep pink", "Deep sky blue",
              "Dim gray", "Dodger blue", "Firebrick", "Floral white", "Forest green", "Fuchsia", "Gainsboro",
              "Ghost white", "Gold", "Goldenrod", "Gray", "Green", "Green yellow", "Honeydew", "Hot pink",
              "Indian red", "Indigo", "Ivory", "Khaki", "Lavender", "Lavender blush", "Lawn green", "Lemon chiffon",
              "Light blue", "Light coral", "Light cyan", "Light goldenrod yellow", "Light green", "Light grey",
              "Light pink", "Light salmon", "Light sea green", "Light sky blue", "Light slate gray", "Light steel blue",
              "Light yellow", "Lime", "Lime green", "Linen", "Magenta", "Maroon", "Medium aquamarine", "Medium blue",
              "Medium orchid", "Medium purple", "Medium sea green", "Medium slate blue", "Medium spring green",
              "Medium turquoise", "Medium violet red", "Midnight blue", "Mint cream", "Misty rose", "Moccasin",
              "Navajo white", "Navy", "Old lace", "Olive drab", "Orange", "Orange red"]

    def get_next_value(self, related_values=None) -> any:
        n = np.random.randint(0, len(self.colors))
        return self.colors[n]
