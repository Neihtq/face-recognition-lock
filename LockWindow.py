import sys
import time
from PyQt5 import QtWidgets
from face_lib import *
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import QThreadPool, Qt


class LockWindow(QtWidgets.QWidget):
    def __init__(self):
        super(LockWindow, self).__init__()
        self.create_UI()
        self.threadpool = QThreadPool()


    def unlock(self):
        self.start_button.setEnabled(False)
        rec_thread = FaceRecognitionThread()
        rec_thread.signals.finished.connect(self.update_UI)

        self.threadpool.start(rec_thread)

    def update_UI(self):
        self.descr_label.setText("Hi, nice to see you again! UNLOCKED")

    def create_UI(self):
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.unlock)
        self.descr_label = QLabel("Place your face in front of your camera.")
        self.descr_label.setAlignment(Qt.AlignCenter)
        vbox = QVBoxLayout()
        vbox.addWidget(self.descr_label)
        vbox.addWidget(self.start_button)

        self.setLayout(vbox)
        self.showFullScreen()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = LockWindow()
    sys.exit(app.exec_())