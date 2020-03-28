import sys
from sys import platform
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class SetupWindow(QtWidgets.QWidget):
    def __init__(self):
        super(SetupWindow, self).__init__()
        self.createView()

    def createView(self):
        title_label = QLabel("Welcome! We need to take a picture from you!")
        descr_label = QLabel("Please align your face centered in the fame and click on the button to take picture.\n This Picture will be used for your secure lock. You can change it later.")

        self.cam = QCameraInfo.availableCameras()
        if not self.cam:
            pass

        self.exist = QCameraViewfinder()
        self.exist.show()

        vbox = QVBoxLayout()
        vbox.addWidget(title_label)
        vbox.addWidget(descr_label)

        self.setLayout(vbox)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = SetupWindow()
    sys.exit(app.exec_())