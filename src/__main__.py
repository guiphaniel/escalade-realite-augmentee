import cv2
import mediapipe as mp
from src.controllers.utils.detectors import pose_detector

mp_drawing = mp.solutions.mediapipe.python.solutions.drawing_utils
mp_drawing_styles = mp.solutions.mediapipe.python.solutions.drawing_styles
mp_pose = mp.solutions.mediapipe.python.solutions.pose

# For webcam input:
cap = cv2.VideoCapture(0)
singlePoseDetector = pose_detector.PoseDetector()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
    
    results = singlePoseDetector.detectLandmarks(image)

    if not results:
        continue
    # Draw the pose annotation on the image.    
    mp_drawing.draw_landmarks(
        image,
        results,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
        break
del singlePoseDetector
cap.release()

