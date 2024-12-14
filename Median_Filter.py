"""
    Module Documentation:
    This module is used to apply median filter to an image.
    The median filter replaces each pixel's value with the median
    value of the pixels in the neighborhood.
    The size of the neighborhood is specified by the user.
    The median filter is a non-linear filter.
    The median filter is used to remove salt and pepper noise from an image.
    The median filter is used to remove impulse/random noise from an image.
"""

from os import sys
from PIL import Image
import numpy as np

class MedianFilter:
    """
    Class Documentation:
    This class is used to apply median filter to an image.
    The median filter replaces each pixel's 
    value with the median value of the pixels in the neighborhood.
    
    Attributes:
    input_path: The path of the input image file.
    image: The input image.
    
    Methods:
    __init__: The constructor method used to initialize the class attributes.
    median_filter_custom: The method used to apply median filter to an image.
    process_image: The method used to process the image.
    original_image_size: The method used to get the size of the original image.
    new_image_size: The method used to get the size of the new image.
    
    """

    def __init__(self, input_path=None):
        """Constructor Documentation
        This method is used to initialize the class attributes.
        
        Args:
        input_path: The path of the input image file.
        
        Returns:
        None
        
        """
        self.input_path = input_path
        try:
            self.image = Image.open(input_path).convert("L")
        except FileNotFoundError:
            print("File not found")
            sys.exit(1)

    def median_filter_custom(self, image_array, size=3):
        """Function Documentation
        This function is used to apply median filter to an image.
        The median filter replaces each pixel's 
        value with the median value of the pixels in the neighborhood.
        
        Args:
        image_array: The input image array.
        size: The size of the neighborhood.
        
        Returns:
        filtered_img: The filtered image array.
        
        """
        pad = size // 2
        padded_img = np.pad(image_array, pad, mode="constant", constant_values=0)
        filtered_img = np.zeros_like(image_array)

        for i in range(image_array.shape[0]):
            for j in range(image_array.shape[1]):
                window = padded_img[i : i + size, j : j + size]
                filtered_img[i, j] = np.median(window)

        return filtered_img

    def process_image(self, size=3):
        """Function Documentation
        This function is used to process the image.
        
        Args:
        size: The size of the neighborhood.
        
        Returns:
        filtered_image: The filtered image.
        """
        image_array = np.array(self.image)

        filtered_image_array = self.median_filter_custom(image_array, size)

        filtered_image = Image.fromarray(filtered_image_array)

        output_path = "filtered/" + self.input_path.split("/")[-1].split(".")[0] + "_median_filtered.jpg"
        filtered_image.save(output_path)
        return filtered_image

