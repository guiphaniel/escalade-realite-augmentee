import threading
from abc import abstractmethod

import cv2
import numpy as np
import pygame.draw

from src.controllers.utils.camera import Camera
from src.controllers.utils.detectors import pose_detector


class GameMultiPlayer:

    @abstractmethod
    def __init__(self, manager):
        self.manager = manager
        self.transfoResults = None
        self.cap = None
        self.multiMediapipeWidth = None
        self.image = None
        self.running = False
        self.playersPosition = {0:{},1:{}}
        thMediapipe = threading.Thread(target=self.startMultiMediaPipe)
        thMediapipe.start()
        thPlayer1Position = threading.Thread(target=self.setPlayer1Position)
        thPlayer1Position.start()
        thPlayer2Position = threading.Thread(target=self.setPlayer2Position)
        thPlayer2Position.start()

    @abstractmethod
    def execute(self):
        pass

    def startResultLeft(self):
        leftPoseDetector = pose_detector.PoseDetector()
        while self.running:
            if self.image is None:
                continue
            left = self.image.copy()
            cv2.rectangle(left, (self.multiMediapipeWidth + 100, 0), (1920, 1080), (0, 0, 0), -1)
            resultleft = leftPoseDetector.detectLandmarks(left)
            if resultleft:
                self.transfoResults[0] = self.manager.wallCalibration.getTransformateLandmarks(resultleft)
        del leftPoseDetector

    def startResultRight(self):
        rightPoseDetector = pose_detector.PoseDetector()
        while self.running:
            if self.image is None:
                continue
            right = self.image.copy()
            cv2.rectangle(right, (0, 0), (self.multiMediapipeWidth - 100, 1080), (0, 0, 0), -1)
            resultsright = rightPoseDetector.detectLandmarks(right)
            if resultsright:
                self.transfoResults[0] = self.manager.wallCalibration.getTransformateLandmarks(resultsright)
        del rightPoseDetector

    def startMultiMediaPipe(self):
        # For webcam input:
        self.cap = Camera(1)
        self.running = True
        self.transfoResults = [None, None]
        thLeft = threading.Thread(target=self.startResultLeft)
        thLeft.start()
        thRight = threading.Thread(target=self.startResultRight)
        thRight.start()
        tmp = np.dot(np.linalg.inv(self.manager.wallCalibration.projectiveMatrix), [[1920 // 2], [0], [1]])
        self.multiMediapipeWidth = int((tmp[0] // tmp[2])[0])

        while self.running:
            success, self.image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            if cv2.waitKey(5) & 0xFF == 27:
                break
        thLeft.join()
        thRight.join()

    def closeCam(self):
        self.running = False

    def setPlayer1Position(self):
        while self.running:
            if self.transfoResults is None:
                continue
            if self.transfoResults[0]:
                landmark = self.transfoResults[0].landmark
                for n in [15, 16]:
                    if -100 <= landmark[n].x * 1920 <= 2100 and -100 <= landmark[n].y * 1080 <= 1200 and -100 <= landmark[n + 2].x * 1920 <= 2100 and -100 <= landmark[n + 2].y * 1080 <= 1200 and -100 <= landmark[n + 4].x * 1920 <= 2100 and -100 <= landmark[n + 4].y * 1080 <= 1200 and -100 <= landmark[n + 6].x * 1920 <= 2100 and -100 <= landmark[n + 6].y * 1080 <= 1200:
                        self.playersPosition[0][n] = (pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[n].x * 1920, landmark[n].y * 1080), (landmark[n + 2].x * 1920, landmark[n + 2].y * 1080),(landmark[n + 4].x * 1920, landmark[n + 4].y * 1080),(landmark[n + 6].x * 1920, landmark[n + 6].y * 1080))))

                for n in [27, 28]:
                    if -100 <= landmark[n].x * 1920 <= 2100 and -100 <= landmark[n].y * 1080 <= 1200 and -100 <= landmark[n + 2].x * 1920 <= 2100 and -100 <= landmark[n + 2].y * 1080 <= 1200 and -100 <= landmark[n + 4].x * 1920 <= 2100 and -100 <= landmark[n + 4].y * 1080 <= 1200:
                        self.playersPosition[0][n] = (pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[n].x * 1920, landmark[n].y * 1080), (landmark[n + 2].x * 1920, landmark[n + 2].y * 1080),(landmark[n + 4].x * 1920, landmark[n + 4].y * 1080))))

    def setPlayer2Position(self):
        while self.running:
            if self.transfoResults is None:
                continue
            if self.transfoResults[1]:
                landmark = self.transfoResults[1].landmark
                for n in [15, 16]:
                    if -100 <= landmark[n].x * 1920 <= 2100 and -100 <= landmark[n].y * 1080 <= 1200 and -100 <= landmark[n + 2].x * 1920 <= 2100 and -100 <= landmark[n + 2].y * 1080 <= 1200 and -100 <= landmark[n + 4].x * 1920 <= 2100 and -100 <= landmark[n + 4].y * 1080 <= 1200 and -100 <= landmark[n + 6].x * 1920 <= 2100 and -100 <= landmark[n + 6].y * 1080 <= 1200:
                        self.playersPosition[1][n] = (pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[n].x * 1920, landmark[n].y * 1080), (landmark[n + 2].x * 1920, landmark[n + 2].y * 1080),(landmark[n + 4].x * 1920, landmark[n + 4].y * 1080),(landmark[n + 6].x * 1920, landmark[n + 6].y * 1080))))

                for n in [27, 28]:
                    if -100 <= landmark[n].x * 1920 <= 2100 and -100 <= landmark[n].y * 1080 <= 1200 and -100 <= landmark[n + 2].x * 1920 <= 2100 and -100 <= landmark[n + 2].y * 1080 <= 1200 and -100 <= landmark[n + 4].x * 1920 <= 2100 and -100 <= landmark[n + 4].y * 1080 <= 1200:
                        self.playersPosition[1][n] = (pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[n].x * 1920, landmark[n].y * 1080), (landmark[n + 2].x * 1920, landmark[n + 2].y * 1080),(landmark[n + 4].x * 1920, landmark[n + 4].y * 1080))))

