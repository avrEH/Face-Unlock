
import os
import cv2
import time
from typing import Tuple

def get_face_detector():
    # Use OpenCV's built-in Haar cascade path
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    if not os.path.exists(cascade_path):
        raise FileNotFoundError(f"Haar cascade not found at {cascade_path}")
    return cv2.CascadeClassifier(cascade_path)

def detect_faces_bgr(image_bgr, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    detector = get_face_detector()
    faces = detector.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)
    return faces, gray

def crop_face(gray, x, y, w, h, size: Tuple[int, int]=(200, 200)):
    face = gray[y:y+h, x:x+w]
    return cv2.resize(face, size)

def draw_faces(image_bgr, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(image_bgr, (x, y), (x+w, y+h), (0, 255, 0), 2)

def beep():
    try:
        import winsound
        winsound.Beep(1000, 150)
    except Exception:
        pass

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
