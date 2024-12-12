"""
Module Documentation:
This module is used to apply JPEG compression to an image.
The JPEG compression is a lossy compression technique.
It is based on the fact that the human eye is less sensitive to high-frequency components.
Steps of JPEG compression:
1. Convert the image to YCbCr color space.
2. Apply DCT to the image.
3. Quantize the DCT coefficients.
4. Huffman encode & run-length encode the quantized coefficients.
5. Store the encoded coefficients.
"""

import numpy as np
from os import sys
from PIL import Image
from scipy.fftpack import dct  as DCT
from scipy.fftpack import idct  as IDCT

class Compressor:
    def __init__(self,image_path, quality=100):
        """
        Class Documentation:
        This class is used to apply JPEG compression to an image.
        Args:
        image_path: The path of the input image file.
        quality: The quality of the compressed image.

        Attributes:
        quality: The quality of the compressed image.
        image_path: The path of the input image file.
        quant_matrix: The quantization matrix.
        image: The input image.
        """
        self.quality = quality
        self.image_path = image_path
        self.quant_matrix = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                      [12, 12, 14, 19, 26, 58, 60, 55],
                                      [14, 13, 16, 24, 40, 57, 69, 56],
                                      [14, 17, 22, 29, 51, 87, 80, 62],
                                      [18, 22, 37, 56, 68, 109, 103, 77],
                                      [24, 35, 55, 64, 81, 104, 113, 92],
                                      [49, 64, 78, 87, 103, 121, 120, 101],
                                      [72, 92, 95, 98, 112, 100, 103, 99]])
        try :
            self.image = Image.open(self.image_path).convert("L")
        except FileNotFoundError:
            print("File not found")
            sys.exit(1)

    def apply_dct(self, sub_image):
        """
        Function Documentation:
        apply Discrete Cosine Transform to the sub-image block
        
        Args:
        sub_image: The sub-image block
        Returns:
        The DCT coefficients of the sub-image block
        """
        return DCT(DCT(sub_image.T, norm='ortho').T, norm='ortho')

    def apply_idct(self, sub_image):
        """
        Function Documentation:
        apply Inverse Discrete Cosine Transform to the sub-image
        Args:
        sub_image: The sub-image block
        Returns:
        The IDCT coefficients of the sub-image block
        """
        return IDCT(IDCT(sub_image.T, norm='ortho').T, norm='ortho')

    def quantize(self, sub_image):
        """
        Function Documentation:
        Quantize the DCT coefficients
        Args:
        sub_image: The sub-image block (8x8)
        Returns:
        The quantized sub-image block
        """
        ret = sub_image
        for i in range(8):
            for j in range(8):
                ret[i, j] = np.round(sub_image[i, j] / (self.quant_matrix[i, j] * self.quality / 100))
        return ret

    def dequantize(self, sub_image):
        """
        Function Documentation:
        Dequantize the sub-image block (8x8)
        Args:
        sub_image: The sub-image block
        Returns:
        The dequantized sub-image block
        """
        ret = sub_image
        for i in range(8):
            for j in range(8):
                ret[i, j] = np.round(sub_image[i, j] * (self.quant_matrix[i, j] * self.quality / 100))
        return ret

    def compress(self,quality=100):
        """
        Function Documentation:
        Compress the image
        Saves the compressed image to the disk (adds a suffix "_compressed" to the original image name)
        Args:
        quality: The quality of the compressed image
        Returns:
        compressed_image: The compressed image
        """
        self.quality = quality
        image = self.image
        image_array = np.array(image)
        h = image_array.shape[0]
        w = image_array.shape[1]

        compressed_image = np.zeros((h, w))

        for i in range(0, h, 8):
            for j in range(0, w, 8):
                block = image_array[i:i+8, j:j+8]
                dct_block = self.apply_dct(block)
                quantized_block = self.quantize(dct_block)
                dequantized_block = self.dequantize(quantized_block)
                idct_block = self.apply_idct(dequantized_block)
                compressed_image[i:i+8, j:j+8] = idct_block

        compressed_image = np.clip(compressed_image, 0, 255)
        compressed_image = Image.fromarray(compressed_image.astype(np.uint8))

        output_path = self.image_path.split(".")[0] + "_compressed.jpg"
        compressed_image.save(output_path)
        return compressed_image