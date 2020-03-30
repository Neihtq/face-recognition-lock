import sys
import cv2


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer


class SetupWindow(QtWidgets.QWidget):
    def __init__(self):
        super(SetupWindow, self).__init__()
        self.createView()

        self.timer = QTimer()
        self.timer.timeout.connect(self.view_cam)
        self.control_btn.clicked.connect(self.control_timer)


    def view_cam(self):
        ret, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        step = channel * width
        q_img = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))


    def control_timer(self):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0)
            self.timer.start(20)

        else:
            self.timer.stop()
            self.cap.release()


    def createView(self):
        title_label = QLabel("Welcome! We need to take a picture from you!")
        descr_label = QLabel("Please align your face centered in the fame and click on the button to take picture.\n This Picture will be used for your secure lock. You can change it later.")
        self.image_label = QLabel()
        self.btn = QtWidgets.QPushButton("Start")
        self.btn.clicked.connect(self.control_timer)
        self.control_btn = QtWidgets.QPushButton("Control")

        vbox = QVBoxLayout()
        vbox.addWidget(title_label)
        vbox.addWidget(descr_label)
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.btn)

        self.setLayout(vbox)
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = SetupWindow()
    sys.exit(app.exec_())