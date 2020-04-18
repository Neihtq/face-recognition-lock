
import numpy as np
import cv2
import face_recognition

from PyQt5.QtCore import QThread, QRunnable, pyqtSignal, QObject, pyqtSlot

CONFIDENCE = 0.5
THRESHOLD = 0.3

def detect(frame):
  clean_image = np.copy(frame)
  net = cv2.dnn.readNetFromDarknet("yolov3-face.cfg", "yolov3-wider_16000.weights")
  ln = net.getLayerNames()
  ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

  (H, W) = frame.shape[:2]
  blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
  net.setInput(blob)
  layerOutputs = net.forward(ln)

  boxes = []
  confidences = []
  classIDs = []

  for output in layerOutputs:
    for detection in output:
      scores = detection[5:]
      classID = np.argmax(scores)
      confidence = scores[classID]

      if confidence > CONFIDENCE:
        box = detection[0:4] * np.array([W, H, W, H])
        (center_x, center_y, width, height) = box.astype("int")

        x = int(center_x - (width / 2))
        y = int(center_y - (height / 2))

        boxes.append([x, y, int(width), int(height)])
        confidences.append(float(confidence))
        classIDs.append(classID)

  idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, THRESHOLD)
  has_face = False
  if len(idxs) > 0:
    for i in idxs.flatten():
      (x, y) = (boxes[i][0], boxes[i][1])
      (w, h) = (boxes[i][2], boxes[i][3])
      cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 2)
    has_face = True

  return frame, clean_image, has_face

class WorkerSignals(QObject):
  finished = pyqtSignal()
  result = pyqtSignal(bool)


class FaceRecognitionThread(QRunnable):
  def __init__(self):
    super(FaceRecognitionThread, self).__init__()
    self.signals = WorkerSignals()


  @pyqtSlot()
  def run(self):
    result = self.recognize()
    self.signals.finished.emit()


  def recognize(self):
    cap = cv2.VideoCapture(0)
    known_image = face_recognition.load_image_file("face.jpg")
    known_encoding = face_recognition.face_encodings(known_image)
    process_this_frame = True

    while True:
      ret, unknown_img = cap.read()
      
      small_frame = cv2.resize(unknown_img, (0, 0), fx=0.25, fy=0.25)
      rgb_small_frame = small_frame[:, :, ::-1]

      if process_this_frame:
          face_locations = face_recognition.face_locations(rgb_small_frame)
          face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
          
          for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encoding, face_encoding)
            if True in matches:
              return True

      process_this_frame = not process_this_frame