from PIL import Image
import numpy as np

class ImageFiler:
    def __init__(self):
        self.image = None
        self.filtered_image = None
        self.width = None
        self.height = None

    def load_image(self, image_file):
        self.image = Image.open(image_file)
        self.width, self.height = self.image.size

    def apply_filter(self, kernel_size):
        # Convert image to numpy array
        image_array = np.array(self.image)
        
        # Handle color images
        if len(image_array.shape) == 3:
            # Create a new array to store the blurred image with the same shape as the original
            blurred_image = np.zeros_like(image_array, dtype=np.uint8)
            
            # Process each color channel separately
            for channel in range(image_array.shape[2]):
                channel_array = image_array[:,:,channel]
                blurred_channel = self._blur_channel(channel_array, kernel_size)
                blurred_image[:,:,channel] = blurred_channel
        else:
            # Grayscale image
            blurred_image = self._blur_channel(image_array, kernel_size)
        
        self.filtered_image = Image.fromarray(blurred_image)

    def _blur_channel(self, channel_array, kernel_size):
        padding = kernel_size // 2
        height, width = channel_array.shape
        blurred_channel = np.zeros_like(channel_array, dtype=np.uint8)
        
        # Extend the array with border pixels for better edge handling
        padded_array = np.pad(channel_array, pad_width=padding, mode='edge')
        
        for y in range(height):
            for x in range(width):
                window = padded_array[y:y+kernel_size, x:x+kernel_size]
                blurred_channel[y, x] = int(np.clip(window.mean(), 0, 255))
        
        return blurred_channel

    def save_image(self, output_file):
        self.filtered_image.save(output_file)

    def display_images(self):
        self.image.show()
        self.filtered_image.show()
