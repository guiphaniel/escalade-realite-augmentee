import cv2
import mediapipe as mp
from src.controllers.utils.detectors import pose_detector
from src.controllers.utils.transform import Transform
from src.model.components.player import Player
import mediapipe as mp
import copy

mp_drawing = mp.solutions.mediapipe.python.solutions.drawing_utils
mp_drawing_styles = mp.solutions.mediapipe.python.solutions.drawing_styles
mp_pose = mp.solutions.mediapipe.python.solutions.pose

wallCalibration = Transform()
wallCalibration.startCalibration()



# For webcam input:
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
print (cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print (cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
photo= cv2.imread("D:/Git/ptut/src/view/images/BlackScreen.png")
singlePoseDetector = pose_detector.PoseDetector()

while cap.isOpened():
    success, image = cap.read()
    outImg=copy.copy(photo)
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
    
    results = singlePoseDetector.detectLandmarks(image)
    if not results:
        continue

    transfoResults= wallCalibration.getTransformateLandmarks(results)

    # Draw the pose annotation on the image.   
     
    mp_drawing.draw_landmarks(
        outImg,
        #results,
        transfoResults,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    
    # Flip the image horizontally for a selfie-view display.
    cv2.namedWindow('MediaPipe Pose', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('MediaPipe Pose',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow('MediaPipe Pose',outImg)
    if cv2.waitKey(5) & 0xFF == 27:
        break
del singlePoseDetector
cap.release()

