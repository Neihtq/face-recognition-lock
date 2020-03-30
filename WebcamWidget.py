import numpy as np
from PyQt5 import QtWidgets, QtGui

class WebcamWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage()

    def image_data_slot(self, image_data):
        self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()


    def get_qimage(self, image: np.ndarray):
        h, w, c = image.shape
        bytes_per_line = 3 * w

        image = QtGui.QImage(image.data,
                             w, h, bytes_per_line,
                             QtGui.QImage.Format_RGB888)
        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()