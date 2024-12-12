from JPEG_Compression import Compressor

comp1 = Compressor("Parrot_Grey.png",80)
comp2 = Compressor("Parrot.jpg",80)
comp1.compress()
comp2.compress()


print("Done")       