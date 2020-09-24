import cv2

def detect(direction):
    capture = cv2.VideoCapture(0)
    for i in range(10000):
        ret, frame = capture.read()
        cv2.imshow('title',frame)
    capture.release()

detect(0)