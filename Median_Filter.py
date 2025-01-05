import numpy as np
from PIL import Image
import os


class MedianFilter:
    """
    Class Documentation:
     This class is used to apply a median filter to an image or a custom array.
     The median filter replaces each pixel's value with the median value of the pixels in the neighborhood.

    Attributes:
     input_path: The path of the input image file.
     image: The input image.

    Methods:
     __init__: The constructor method used to initialize the class attributes.
     median_filter_custom: The method used to apply median filter to an image or array.
     process_image: The method used to process the image.
    """

    def __init__(self, input_path=None):
        """Constructor Documentation"""
        self.input_path = input_path
        if input_path:
            try:
                self.image = Image.open(input_path).convert("L")
            except FileNotFoundError:
                print("File not found")
                exit(1)
        else:
            self.image = None

    def median_filter_custom(self, image_array, size=3, method="padding"):
        """Applies median filter to an image or array"""

        pad = size // 2

        if method == "padding":
            padded_img = np.pad(image_array, pad, mode="constant", constant_values=0)
            filtered_img = np.zeros_like(image_array)
        elif method == "reflect":
            padded_img = np.pad(image_array, pad, mode="reflect")
            filtered_img = np.zeros_like(image_array)
        elif method == "edge":
            padded_img = np.pad(image_array, pad, mode="edge")
            filtered_img = np.zeros_like(image_array)
        elif method == "symmetric":
            padded_img = np.pad(image_array, pad, mode="symmetric")
            filtered_img = np.zeros_like(image_array)
        elif method == "crop":
            filtered_img = np.zeros(
                (image_array.shape[0] - 2 * pad, image_array.shape[1] - 2 * pad)
            )
        else:
            raise ValueError(
                "Invalid method. Choose from 'padding', 'reflect', 'edge', 'symmetric', 'crop'."
            )

        for i in range(image_array.shape[0]):
            for j in range(image_array.shape[1]):
                if method == "crop":
                    if (
                        i >= pad
                        and i < image_array.shape[0] - pad
                        and j >= pad
                        and j < image_array.shape[1] - pad
                    ):
                        window = image_array[
                            i - pad : i + pad + 1, j - pad : j + pad + 1
                        ]
                        filtered_img[i - pad, j - pad] = np.median(window)
                else:
                    window = padded_img[i : i + size, j : j + size]
                    filtered_img[i, j] = np.median(window)

        return filtered_img

    def process_image(self, size=3, method="padding"):
        """Processes the image using the chosen edge-handling method"""

        if self.image is None:
            raise ValueError("No image loaded to process")

        image_array = np.array(self.image)

        filtered_image_array = self.median_filter_custom(image_array, size, method)

        filtered_image = Image.fromarray(filtered_image_array.astype(np.uint8))

        output_dir = "filtered"
        os.makedirs(output_dir, exist_ok=True)

        output_path = f"{output_dir}/{os.path.basename(self.input_path).split('.')[0]}_median_filtered.jpg"
        filtered_image.save(output_path)

        return filtered_image


def test_filter_on_custom_array_median():
    """
    This function allows the user to input a custom array and test the median filter
    with different methods for edge handling.
    """
    print(
        "Enter a 2D array (as a list of lists). Example: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]"
    )
    user_input = input("Your 2D array: ")

    try:
        custom_array = np.array(eval(user_input))
        if custom_array.ndim != 2:
            raise ValueError("Please enter a valid 2D array.")

        print("\nOriginal Array:")
        print(custom_array)

        size = int(input("Enter the filter size (e.g., 3 for a 3x3 filter): "))
        method = input(
            "Choose an edge-handling method (padding, crop, reflect, edge, symmetric): "
        )

        filter_obj = MedianFilter()
        filtered_array = filter_obj.median_filter_custom(custom_array, size, method)

        print(f"\nFiltered Array (Method: {method}):")
        print(filtered_array)
    except Exception as e:
        print(f"An error occurred: {e}")


# Calling the function for testing
# test_filter_on_custom_array_median()
