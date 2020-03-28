import sys
from sys import platform
from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

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


    def createUI(self):
        self.showFullScreen()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = LockWindow()
    sys.exit(app.exec_())