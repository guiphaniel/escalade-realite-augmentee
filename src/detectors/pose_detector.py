import cv2
import mediapipe as mp

def detectLandmarks(image, pose):
        results = pose.process(image)
        return results