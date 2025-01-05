# 🖼️ Noise Reduction & JPEG Compression

This project is a simple implementation of noise reduction and JPEG compression using Python. The project is divided into two parts, the first part is noise reduction and the second part is JPEG compression.

## 👥 Contributors

- [Mahmoud Sameh](https://github.com/MhmudSameh24)
- [Mazen Ghanayem](https://github.com/Mazen-Ghanaym)
- [Youssef Gaber](https://github.com/Yousef-Gaber11)
- [Ahmed M. Wahba](https://github.com/abowahbaz)
- [Islam Imad](https://github.com/Islam-Imad)
- [Mohamed Mahmoud](https://github.com/mohammedmoud)

## ✨ Features

- Noise Reduction Using Median Filter
- Noise Reduction Using Average Filter
- JPEG Compression

## 📦 Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.6** or higher installed on your machine.
- **PyQt** as the GUI library.
- **Pillow** for image processing.
- **SciPy** for image processing and mathematical operations.

## 🛠️ Installation

1. First,clone the repository using the following command:

```bash
git clone https://github.com/abowahbaz/Image_Processing_App.git
```

2. Install the required libraries using the following command:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Run the application using the following command:

```bash
python home.py
```

Or just double click `Run Project.bat` file and it will do all the previous steps for you 😉.

---

1. Choose the desired operation from the main menu.
   ![Home](./ReadMe%20Images/home.png)


2. JPEG Compression:

   - Choose the image you want to compress.
   - Click the compress button.

    <img src = "./ReadMe%20Images/jpeg_choose.png" width = "500"/>

   - The compressed image will be saved in the `Compressed` folder.

    <img src = "./ReadMe%20Images/jpeg_compare.png" width = "500"/>

   - the old image and the compressed image will be displayed in the GUI window,as well as the compression ratio, with sizes comparison.

3. Noise Reduction:

   - Choose the image you want to reduce noise from.
   - Choose the filter type (Median or Average).
   - Choose the filter size.
   - Choose the edge handling method.
   - Click the filter button.

    <img src = "./ReadMe%20Images/noise_choose.png" width = "500"/>

   - The filtered image will be saved in the `Filtered` folder.

    <img src = "./ReadMe%20Images/noise_compare.png" width = "500"/>

   - the old image and the filtered image will be displayed in the GUI window.

## 📁 Project Structure

`home.py` : The main file that contains the GUI implementation.

`JPEG_Compression.py` : The file that contains the JPEG compression implementation.

`Median_Filter.py` : The file that contains the median filter implementation.

`Average_Filter.py` : The file that contains the average filter implementation.

`Compressed` : The folder that contains the compressed images.

`Filtered` : The folder that contains the filtered images.

`jpeg_ui` ,`jpeg_compare.ui` ,`noise_ui` ,`noise_compare.ui` : The GUI files.

## 🤝 Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

## 🙏 Acknowledgments

- **PyQt** : For the GUI library.
- **Pillow** : For image processing.
- **SciPy** : For image processing and mathematical operations.
