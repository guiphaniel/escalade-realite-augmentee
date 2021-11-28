import cv2
import mediapipe as mp
from src.controllers.utils.detectors import pose_detector
from src.model.components.player import Player

mp_drawing = mp.solutions.mediapipe.python.solutions.drawing_utils
mp_drawing_styles = mp.solutions.mediapipe.python.solutions.drawing_styles
mp_pose = mp.solutions.mediapipe.python.solutions.pose

# For webcam input:
cap = cv2.VideoCapture(0)
landmarks_enum = mp.solutions.mediapipe.python.solutions.pose.PoseLandmark
player1 = Player("Guilhem")
player1PoseDetector = pose_detector.PoseDetector()


while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
    
    player1Landmarks = player1PoseDetector.detectLandmarks(image)   

    if not player1Landmarks:          
        continue
    
    print(player1Landmarks.landmark[landmarks_enum.NOSE].x)
    
    
    # Draw the pose annotation on the image.    
    mp_drawing.draw_landmarks(
        image,
        player1Landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
        break
del player1PoseDetector
cap.release()

