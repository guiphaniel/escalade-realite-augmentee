import cv2
import mediapipe as mp

class PoseDetector:
  
    # Initializing
    def __init__(self):
        self.mp_pose = mp.solutions.mediapipe.python.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)  
        
    # Deleting (Calling destructor)
    def __del__(self):
        self.pose.close()


    def detectLandmarks(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return results

