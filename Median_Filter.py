from PIL import Image
import numpy as np

class Median_Filter:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path).convert('L')
        self.image_array = np.array(self.image)

    def median_filter_custom(self, size=3):
        pad = size // 2
        padded_img = np.pad(self.image_array, pad, mode='constant', constant_values=0)
        
        filtered_img = np.zeros_like(self.image_array)

        for i in range(self.image_array.shape[0]):
            for j in range(self.image_array.shape[1]):
                window = padded_img[i:i+size, j:j+size]
                filtered_img[i, j] = np.median(window)

        return filtered_img

    def show_filtered_image(self, size=3):
        filtered_image = self.median_filter_custom(size)
        filtered_image_pil = Image.fromarray(filtered_image)
        filtered_image_pil.show()

run = Median_Filter(r'D:\PythonVS\IMG_Median\SP_Pics\2.jpeg')
run.show_filtered_image(size=3)
