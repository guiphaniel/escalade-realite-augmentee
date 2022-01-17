import threading
from abc import abstractmethod

import cv2

from src.controllers.utils.detectors import pose_detector


class Game:

    @abstractmethod
    def __init__(self,manager):
        self.manager=manager
        self.transfoResults=None
        self.cap=None
        th = threading.Thread(target=self.startCam)
        th.start()

    @abstractmethod
    def execute(self):
        pass

    def startCam(self):
        singlePoseDetector = pose_detector.PoseDetector()
        self.cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            results = singlePoseDetector.detectLandmarks(image)
            if not results:
                continue

            self.transfoResults = self.manager.wallCalibration.getTransformateLandmarks(results)
            print("after",self.transfoResults.landmark[15].x*1920)


    def closeCam(self):
        self.cap.release()