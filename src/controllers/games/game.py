import copy
import os
import threading
from abc import abstractmethod
import mediapipe as mp
import cv2
import pygame.draw

from src.controllers.utils.camera import Camera
from src.controllers.utils.detectors import pose_detector



class Game:

    @abstractmethod
    def __init__(self,manager):
        self.manager=manager
        self.continueGame=False
        self.transfoResults=None
        self.cap=None
        th = threading.Thread(target=self.startCam)
        th.start()

    @abstractmethod
    def execute(self):
        pass

    def startCam(self):
        # For webcam input:
        self.cap = Camera(1)
        self.continueGame=True
        singlePoseDetector = pose_detector.PoseDetector()

        while self.continueGame:
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            results = singlePoseDetector.detectLandmarks(image)
            if not results:
                continue

            self.transfoResults = self.manager.wallCalibration.getTransformateLandmarks(results)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        del singlePoseDetector

    def closeCam(self):
        self.continueGame=False

    def getPlayerPosition(self):
        if self.transfoResults:
            landmark = self.transfoResults.landmark
            playerPosition = [pygame.draw.polygon(self.manager.screen, (0, 0, 255), (
            (landmark[15].x * 1920, landmark[15].y * 1080), (landmark[17].x * 1920, landmark[17].y * 1080),
            (landmark[19].x * 1920, landmark[19].y * 1080))),
                              pygame.draw.polygon(self.manager.screen, (0, 0, 255), (
                              (landmark[16].x * 1920, landmark[16].y * 1080),
                              (landmark[18].x * 1920, landmark[18].y * 1080),
                              (landmark[20].x * 1920, landmark[20].y * 1080))),
                              pygame.draw.polygon(self.manager.screen, (0, 0, 255), (
                              (landmark[27].x * 1920, landmark[27].y * 1080),
                              (landmark[29].x * 1920, landmark[29].y * 1080),
                              (landmark[31].x * 1920, landmark[31].y * 1080))),
                              pygame.draw.polygon(self.manager.screen, (0, 0, 255), (
                              (landmark[28].x * 1920, landmark[28].y * 1080),
                              (landmark[30].x * 1920, landmark[30].y * 1080),
                              (landmark[32].x * 1920, landmark[32].y * 1080)))]
            return playerPosition
        return []
