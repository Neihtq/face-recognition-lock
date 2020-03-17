import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
frame_id = 0

while True:
    _, frame = cap.read()
    frame_id += 1
    (H, W) = frame.shape[:2]

    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi = frame[y:y+h, x:x+w]

    cv2.imshow("Image", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()