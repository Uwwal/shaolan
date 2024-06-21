import os.path
from io import BytesIO

from PIL import Image

from config.constant import wums_dir, wums_rarity_dict
from utils.image_utils import image_to_square


class Wum:
    def __init__(self, file_name):
        self.name = os.path.splitext(file_name)[0]
        self.rarity = wums_rarity_dict[self.name]

        path = os.path.join(wums_dir, file_name)

        image = Image.open(path)
        image_square = image_to_square(image)

        self.buf = BytesIO()
        image_square.save(self.buf, format='PNG')

        image.close()

    def __eq__(self, other):
        if isinstance(other, Wum):
            return self.name == other.name
        return False
