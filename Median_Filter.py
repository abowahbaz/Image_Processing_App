"""
    Module Documentation:
    TODO
"""

from PIL import Image
import numpy as np


class MedianFilter:
    """
    Class Documentation:
    """
    def __init__(self, input_path=None):
        """ Constructor Documentation """
        self.input_path = input_path
        try:
            self.image = Image.open(input_path).convert("L")
        except FileNotFoundError:
            print("File not found")
            exit(1)

    def median_filter_custom(self, image_array, size=3):
        """ Function Documentation """
        pad = size // 2
        padded_img = np.pad(image_array, pad, mode="constant", constant_values=0)
        filtered_img = np.zeros_like(image_array)

        for i in range(image_array.shape[0]):
            for j in range(image_array.shape[1]):
                window = padded_img[i : i + size, j : j + size]
                filtered_img[i, j] = np.median(window)

        return filtered_img

    def process_image(self, size=3):
        """ Function Documentation """ 
        image_array = np.array(self.image)

        filtered_image_array = self.median_filter_custom(image_array, size)

        filtered_image = Image.fromarray(filtered_image_array)
        
        output_path = self.input_path.split(".")[0] + "_filtered.png"
        filtered_image.save(output_path)

    def original_image_size(self):
        """ Function Documentation """
        return self.image.size

    def new_image_size(self):
        """ Function Documentation """
        return self.image.size


app = MedianFilter("download.jpeg")
app.process_image(3)
print(app.original_image_size())
print(app.new_image_size())