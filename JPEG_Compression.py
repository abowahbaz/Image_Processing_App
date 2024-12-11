import numpy as np
from PIL import Image
from scipy.fftpack import dct  as DCT
from scipy.fftpack import idct  as IDCT

class Compressor:
    def __init__(self, quality=100):
        self.quality = quality
        self.quant_matrix = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                      [12, 12, 14, 19, 26, 58, 60, 55],
                                      [14, 13, 16, 24, 40, 57, 69, 56],
                                      [14, 17, 22, 29, 51, 87, 80, 62],
                                      [18, 22, 37, 56, 68, 109, 103, 77],
                                      [24, 35, 55, 64, 81, 104, 113, 92],
                                      [49, 64, 78, 87, 103, 121, 120, 101],
                                      [72, 92, 95, 98, 112, 100, 103, 99]])

    def apply_dct(self, sub_image):
        return DCT(DCT(sub_image.T, norm='ortho').T, norm='ortho')

    def apply_idct(self, sub_image):
        return IDCT(IDCT(sub_image.T, norm='ortho').T, norm='ortho')

    def quantize(self, sub_image):
        ret = sub_image
        for i in range(8):
            for j in range(8):
                ret[i, j] = np.round(sub_image[i, j] / (self.quant_matrix[i, j] * self.quality / 100))
        return ret

    def dequantize(self, sub_image):
        ret = sub_image
        for i in range(8):
            for j in range(8):
                ret[i, j] = np.round(sub_image[i, j] * (self.quant_matrix[i, j] * self.quality / 100))
        return ret

    def compress(self, input_path, output_path, quality=100):
        self.quality = quality
        image = Image.open(input_path)
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
        compressed_image.save(output_path + '.jpg', 'JPEG', quality=self.quality)


#type:ignore