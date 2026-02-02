import cv2
import numpy as np
from scipy.spatial import distance as dist
import face_recognition


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)


def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[2], mouth[10])
    B = dist.euclidean(mouth[4], mouth[8])
    C = dist.euclidean(mouth[0], mouth[6])
    return (A + B) / (2.0 * C)


def check_liveness(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_landmarks = face_recognition.face_landmarks(rgb)

    if not face_landmarks:
        return False

    landmarks = face_landmarks[0]

    left_eye = landmarks['left_eye']
    right_eye = landmarks['right_eye']
    mouth = landmarks['top_lip'] + landmarks['bottom_lip']

    ear = (eye_aspect_ratio(left_eye) +
           eye_aspect_ratio(right_eye)) / 2.0
    mar = mouth_aspect_ratio(mouth)

    blink_detected = ear < 0.2
    mouth_open = mar > 0.5

    return blink_detected or mouth_open
