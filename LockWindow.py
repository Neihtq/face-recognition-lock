import sys
from sys import platform
from PyQt5 import QtWidgets
from face_lib import *
from face_lib import *
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

if platform == "linux" or platform == "linux2":
    print("linux")

elif platform == "win32":
    print("windows")

else:
    print("mac")


class LockWindow(QtWidgets.QWidget):
    def __init__(self):
        super(LockWindow, self).__init__()
        self.createUI()
        self.unlock()


    def unlock(self):
        is_identical = recognize()
        if is_identical:
            self.descr_label.setText("Hi, nice to see you again! UNLOCKED")



    def createUI(self):
        self.descr_label = QLabel("Place your face in front of your camera.")
        self.descr_label.setAlignment(Qt.AlignCenter)
        vbox = QVBoxLayout()
        vbox.addWidget(self.descr_label)

        self.setLayout(vbox)
        self.showFullScreen()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = LockWindow()
    sys.exit(app.exec_())