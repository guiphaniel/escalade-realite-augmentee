import cv2
import mediapipe as mp

class PoseDetector:

    # Initializing
    def __init__(self):
        self.mp_pose = mp.solutions.mediapipe.python.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.storedLandmarks = None

    # Deleting (Calling destructor)
    def __del__(self):
        self.pose.close()


    def detectLandmarks(self, image):
        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB, image)
        results = self.pose.process(image)
        image.flags.writeable = True
        if results.pose_landmarks:
            self.storedLandmarks = results.pose_landmarks
        return self.storedLandmarks

    def getLandmarks(self):
        return self.storedLandmarks