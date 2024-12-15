"""
    Module Documentation:
    This module is used to apply average filter to an image.
    The average filter replaces each pixel's value with the average
    value of the pixels in the neighborhood.
"""

from os import sys
from PIL import Image
import numpy as np

class AverageFilter:
    """
    Class Documentation:
    This class is used to apply average filter to an image.
    The average filter replaces each pixel's 
    value with the average value of the pixels in the neighborhood.
    
    Attributes:
    input_path: The path of the input image file.
    image: The input image.
    
    Methods:
    __init__: The constructor method used to initialize the class attributes.
    average_filter_custom: The method used to apply average filter to an image.
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

    def average_filter_custom(self, image_array, kernel_size=3):
        """Function Documentation
        This function is used to apply average filter to an image.
        The average filter replaces each pixel's 
        value with the average value of the pixels in the neighborhood.
        
        Args:
        image_array: The input image array.
        kernel_size: The size of the neighborhood.
        
        Returns:
        filtered_img: The filtered image array.
        
        """
        height, width = image_array.shape
        padding = kernel_size // 2
        padded_img = np.pad(image_array, padding, mode="edge")
        filtered_img = np.zeros_like(image_array)
        for row in range(height):
            for col in range(width):
                kernel_window = padded_img[row : row + kernel_size, col : col + kernel_size]
                filtered_img[row, col] = int(np.mean(kernel_window))

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

        filtered_image_array = self.average_filter_custom(image_array, size)

        filtered_image = Image.fromarray(filtered_image_array)

        output_path = "filtered/" + self.input_path.split("/")[-1].split(".")[0] + "_average_filtered.jpg"
        filtered_image.save(output_path)
        return filtered_image

    def original_image_size(self):
        """Function Documentation
        This function is used to get the size of the original image.
        
        Returns:
        image.size: The size of the original image.
        """
        return self.image.size

    def new_image_size(self):
        """Function Documentation
        This function is used to get the size of the new image.
        
        Returns:
        self.image.size: The size of the new image. 
        """
        return self.process_image().size
