from os import sys, makedirs
from PIL import Image
import numpy as np
import os


class AverageFilter:
    """
    Class Documentation:
    This class is used to apply an average filter to an image or array.
    The average filter replaces each pixel's
    value with the average value of the pixels in the neighborhood.

    Attributes:
    input_path: The path of the input image file.
    image: The input image.

    Methods:
    __init__: The constructor method used to initialize the class attributes.
    average_filter_custom: The method used to apply average filter to an image or array.
    process_image: The method used to process an image from file.
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
        if input_path:
            try:
                self.image = Image.open(input_path).convert("L")
            except FileNotFoundError:
                print("File not found. Please provide a valid path.")
                sys.exit(1)
        else:
            self.image = None

    def average_filter_custom(self, image_array, size=3, method="padding"):
        """Function Documentation
        This function applies an average filter to an image or array using different edge-handling methods.

        Args:
        image_array: The input 2D array (image or custom array).
        size: The size of the neighborhood (e.g., 3 for a 3x3 filter).
        method: The method for edge handling. Options are:
            - "padding": Add constant padding (default is 0)
            - "crop": Ignore edges, resulting in a smaller output array
            - "reflect": Reflect the image values at the edge
            - "edge": Repeat the edge values
            - "symmetric": Symmetrically mirror the edge values

        Returns:
        filtered_img: The filtered image/array.
        """
        pad = size // 2

        # Handle different padding methods
        if method == "padding":
            padded_img = np.pad(image_array, pad, mode="constant", constant_values=0)
        elif method == "reflect":
            padded_img = np.pad(image_array, pad, mode="reflect")
        elif method == "edge":
            padded_img = np.pad(image_array, pad, mode="edge")
        elif method == "symmetric":
            padded_img = np.pad(image_array, pad, mode="symmetric")
        elif method == "crop":
            filtered_img = np.zeros(
                (image_array.shape[0] - 2 * pad, image_array.shape[1] - 2 * pad)
            )
            # Apply filter with no padding (direct crop)
            for i in range(pad, image_array.shape[0] - pad):
                for j in range(pad, image_array.shape[1] - pad):
                    window = image_array[i - pad : i + pad + 1, j - pad : j + pad + 1]
                    filtered_img[i - pad, j - pad] = np.mean(window)
            return filtered_img.astype(np.uint8)
        else:
            raise ValueError(
                "Invalid method. Choose from 'padding', 'reflect', 'edge', 'symmetric', 'crop'."
            )

        # Applying the filter to the padded image
        filtered_img = np.zeros_like(image_array)
        for i in range(image_array.shape[0]):
            for j in range(image_array.shape[1]):
                window = padded_img[i : i + size, j : j + size]
                filtered_img[i, j] = np.mean(window)

        return filtered_img.astype(np.uint8)

    def process_image(self, size=3, method="padding"):
        """Function Documentation
        This function processes the image using the chosen edge-handling method.

        Args:
        size: The size of the neighborhood.
        method: The method for edge handling. Options are:
            - "padding"
            - "crop"
            - "reflect"
            - "edge"
            - "symmetric"

        Returns:
        filtered_image: The filtered image.
        """

        if self.image is None:
            raise ValueError("No image loaded to process")

        image_array = np.array(self.image)

        filtered_image_array = self.average_filter_custom(image_array, size, method)

        filtered_image = Image.fromarray(filtered_image_array.astype(np.uint8))

        output_dir = "filtered"
        os.makedirs(output_dir, exist_ok=True)

        output_path = f"{output_dir}/{os.path.basename(self.input_path).split('.')[0]}_average_filtered.jpg"
        filtered_image.save(output_path)

        return filtered_image

    def original_image_size(self):
        """Function Documentation
        This function is used to get the size of the original image.

        Returns:
        image.size: The size of the original image.
        """
        return self.image.size if self.image else None

    def new_image_size(self, size=3, method="padding"):
        """Function Documentation
        This function is used to get the size of the new image.

        Returns:
        self.image.size: The size of the new image.
        """
        filtered_image = self.process_image(size, method)
        return filtered_image.size


def test_filter_on_custom_array():
    """
    This function allows the user to input a custom array and test the average filter
    with different methods for edge handling.
    """
    print(
        "Enter a 2D array (as a list of lists). Example: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]"
    )
    user_input = input("Your 2D array: ")

    try:
        custom_array = np.array(eval(user_input))
        print("\nOriginal Array:")
        print(custom_array)

        size = int(input("Enter the filter size (e.g., 3 for a 3x3 filter): "))
        method = input(
            "Choose an edge-handling method (padding, crop, reflect, edge, symmetric): "
        )

        filter_obj = AverageFilter()
        filtered_array = filter_obj.average_filter_custom(custom_array, size, method)

        print(f"\nFiltered Array (Method: {method}):")
        print(filtered_array)
    except Exception as e:
        print(f"An error occurred: {e}")


# Calling the function for testing
# test_filter_on_custom_array()
