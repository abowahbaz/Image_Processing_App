# Basic Imports
import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication,QGraphicsView,QGraphicsScene
from PyQt5 import QtGui
from PyQt5.QtCore import Qt


# Algorithm Imports
from JPEG_Compression import Compressor 
from Median_Filter import MedianFilter
from Average_Filter import AverageFilter



class Home(QMainWindow):
    def __init__(self):
        super(Home, self).__init__()
        loadUi('home.ui', self)
        self.jpeg_button.clicked.connect(self.go_to_jpeg)
        self.noise_button.clicked.connect(self.go_to_noise)

    def go_to_jpeg(self):
       widgets.setCurrentWidget(jpeg)
    
    def go_to_noise(self):
        widgets.setCurrentWidget(noise)


class JPEG(QMainWindow):
    def __init__(self):
        super(JPEG, self).__init__()
        self.reset_fields()

    def reset_fields(self):
        loadUi('jpeg.ui', self)
        self.home_button.clicked.connect(self.to_home)
        self.choose_file_button.clicked.connect(self.add_file)
        self.compress_button.clicked.connect(self.compress)
        self.input_path = ""
        self.output_path = ""


    def handle_visible(self):
        flag = (self.input_path != "")
        self.compress_button.setVisible(flag)
     
      

    def to_home(self):
        self.reset_fields()
        widgets.setCurrentWidget(home)
        
       
        

    def add_file(self):
        self.input_path = ""
        try:
            self.input_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'Images/')[0]
        except:
            print("No file selected")

        self.output_path = "compressed/" + self.input_path.split('/')[-1].split('.')[0] + "_compressed.jpg"          
        self.handle_visible()
        scene = QGraphicsScene()
        pixmap = QtGui.QPixmap(self.input_path)
        scene.addPixmap(pixmap)
        self.image_view.setScene(scene)
        self.image_view.show()
        

    # Compress and view a comparison of the original and compressed images

    def compress(self):
        comp = Compressor(self.input_path)
        comp.compress()
        loadUi('jpeg_compare.ui', self)
        self.home_button.clicked.connect(self.view_to_home)
        self.show_images()

    def view_to_home(self):
        self.old_image_view.setScene(None)
        self.new_image_view.setScene(None)
        self.reset_fields()
        widgets.setCurrentWidget(home)

    def show_images(self):
        scene = QGraphicsScene()
        pixmap = QtGui.QPixmap(self.input_path)
        scene.addPixmap(pixmap)
        self.old_image_view.setScene(scene)
        self.old_image_view.show()
        self.osize_value.setText(f"{os.path.getsize(self.input_path) / 1024:.2f} KB")
        self.nsize_value.setText(f"{os.path.getsize(self.output_path) / 1024:.2f} KB")

        ratio = round(os.path.getsize(self.output_path) / os.path.getsize(self.input_path), 2) # percentage compression
        self.comp_value.setText(f"{ratio * 100:.2f}%")

        scene = QGraphicsScene()
        pixmap = QtGui.QPixmap(self.output_path)
        scene.addPixmap(pixmap)
        self.new_image_view.setScene(scene)
        self.new_image_view.show()


class NoiseReduction(QMainWindow):
    def __init__(self):
        super(NoiseReduction, self).__init__()
        self.reset_fields()

    def reset_fields(self):
        loadUi('noise.ui', self)
        self.choose_file_button.clicked.connect(self.add_file)
        self.home_button.clicked.connect(self.to_home)
        self.filter_button.clicked.connect(self.filter_image)
        self.input_path = ""
        self.output_path = ""
        self.state = False
        self.handle_visible()

    def handle_visible(self):
        self.filter_button.setVisible(self.state)
        self.filter_list.setVisible(self.state)
        self.intensity_box.setVisible(self.state)
        self.state = not self.state

    def to_home(self): # Reset fields and go back to home from noise reduction
        self.reset_fields()
        widgets.setCurrentWidget(home)

    def add_file(self):
        self.input_path = ""
        try:
            self.input_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'Images/')[0]
        except:
            print("No file selected")

        self.handle_visible()
        scene = QGraphicsScene()
        pixmap = QtGui.QPixmap(self.input_path)
        scene.addPixmap(pixmap)
        self.image_view.setScene(scene)
        self.image_view.show()

    def filter_image(self):
        self.output_path = "filtered/" + self.input_path.split('/')[-1].split('.')[0]
        intensity = self.intensity_box.value()
        is_median = self.filter_list.currentText() == "Median Filter"
        if is_median:
            filter = MedianFilter(self.input_path)
            self.output_path += "_median_filtered.jpg"
        else:
            filter = AverageFilter(self.input_path)
            self.output_path += "_average_filtered.jpg"

        filter.process_image(intensity)
        self.show_images()

    def show_images(self):
        loadUi('noise_compare.ui', self)
        self.home_button.clicked.connect(self.view_to_home)
        scene = QGraphicsScene()
        pixmap = QtGui.QPixmap(self.input_path)
        scene.addPixmap(pixmap)
        self.old_image_view.setScene(scene)
        self.old_image_view.show()
        scene = QGraphicsScene()
        pixmap = QtGui.QPixmap(self.output_path)
        scene.addPixmap(pixmap)
        self.new_image_view.setScene(scene)
        self.new_image_view.show()

    def view_to_home(self): # Reset fields and go back to home from noise reduction comparison
        self.old_image_view.setScene(None)
        self.new_image_view.setScene(None)
        self.reset_fields()
        widgets.setCurrentWidget(home)


# ==================================================================================================
# =================================  Main Program  =================================================
app = QApplication(sys.argv)
app.setApplicationName("Image Processing App")
app.setWindowIcon(QtGui.QIcon('icon.png'))
app.setStyle('Fusion')  
home = Home()
jpeg = JPEG()
noise = NoiseReduction()

widgets = QtWidgets.QStackedWidget()
widgets.addWidget(home)
widgets.addWidget(jpeg)
widgets.addWidget(noise)

widgets.setFixedHeight(768)
widgets.setFixedWidth(1024)
widgets.show()



try:
    sys.exit(app.exec_())
except:
    print("Exiting")
