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
    def __init__(self):
        """ Constructor Documentation """
        self.image = None

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

    def process_image(self, input_path, output_path, size=3):
        """ Function Documentation """ 
        image = Image.open(input_path).convert("L")
        image_array = np.array(image)

        filtered_image_array = self.median_filter_custom(image_array, size)

        filtered_image = Image.fromarray(filtered_image_array)
        filtered_image.save(output_path)

    def original_image_size(self, image):
        """ Function Documentation """
        return image.size

    def new_image_size(self, image):
        """ Function Documentation """
        return image.size


run = MedianFilter()
run.process_image(
    input_path=r"test_image.png",
    output_path=r"output_image.png",
)
