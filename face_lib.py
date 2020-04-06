
import numpy as np
import cv2
import face_recognition

CONFIDENCE = 0.5
THRESHOLD = 0.3

def detect(frame):
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
  print(len(idxs))
  if len(idxs) > 0:
    for i in idxs.flatten():
      (x, y) = (boxes[i][0], boxes[i][1])
      (w, h) = (boxes[i][2], boxes[i][3])
      cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 2)
    has_face = True

  return frame, has_face


def recognize():
  cap = cv2.VideoCapture(0)
  known_image = face_recognition.load_image_file("pictures/face.jpg")
  known_encoding = face_recognition.face_encodings(known_image)[0]

  while True:
    ret, unknown_img = cap.read()

    unknown_encoding = face_recognition.face_encodings(unknown_img)[0]
    results = face_recognition.compare_faces([known_encoding], unknown_encoding)

    if results[0] == True:
      return True