import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from face_lib import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer


class SetupWindow(QtWidgets.QWidget):
    SAVED = "Picture saved successfully!"
    NO_FACE = "There is no face found. Please try again."
    CONFIRM = "Is this ok?"
    DESCR = "Please align your face centered in the fame and click on the button to take a picture.\nThis Picture will be used for your secure lock. You can change it later."
    def __init__(self):
        super(SetupWindow, self).__init__()
        self.createView()
        self.timer = QTimer()
        self.timer.timeout.connect(self.view_cam)


    def view_cam(self):
        ret, self.image = self.cap.read()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.update_frame()


    def update_frame(self):
        height, width, channel = self.image.shape
        step = channel * width
        q_img = QImage(self.image.data, width, height, step, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))


    def control_timer(self):
        if not self.timer.isActive():
            self.descr_label.setText(self.DESCR)
            self.btn.setText("Take Picture")
            self.yes_btn.setVisible(False)
            self.cap = cv2.VideoCapture(0)
            self.timer.start(20)
        else:
            self.draw_face_box()
            self.timer.stop()
            self.cap.release()


    def draw_face_box(self):
        self.image, has_face = detect(self.image)
        self.update_frame()
        if has_face:
            self.descr_label.setText(self.CONFIRM)
            self.btn.setText("No")
            self.yes_btn.setVisible(True)
        else:
            self.descr_label.setText()
            self.btn.setText("Okay")


    def createView(self):
        title_label = QLabel("Welcome! We need to take a pictures from you!")
        self.descr_label = QLabel(self.DESCR)

        self.image_label = QLabel()
        self.btn = QtWidgets.QPushButton("Start")
        self.btn.clicked.connect(self.control_timer)
        self.yes_btn = QtWidgets.QPushButton("Yes")
        self.yes_btn.clicked.connect(self.save_image)
        self.yes_btn.setVisible(False)

        vbox = QVBoxLayout()
        vbox.addWidget(title_label)
        vbox.addWidget(self.descr_label)
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.yes_btn)

        self.setLayout(vbox)
        self.show()


    def save_image(self):
        directory = "pictures/face.jpg"
        cv2.imwrite(directory, cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        self.btn.setVisible(False)
        self.yes_btn.setText("Nice!")
        self.yes_btn.clicked.connect(self.exit)
        self.descr_label.setText(self.SAVED)

    def exit(self):
        self.close()
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = SetupWindow()
    sys.exit(app.exec_())