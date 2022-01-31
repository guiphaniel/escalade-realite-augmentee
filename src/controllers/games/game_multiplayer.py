import copy
import os
import threading
from abc import abstractmethod
import mediapipe as mp
import cv2
import numpy as np
import pygame.draw

from src.controllers.utils.camera import Camera
from src.controllers.utils.detectors import pose_detector



class GameMultiPlayer:

    @abstractmethod
    def __init__(self,manager):
        self.manager=manager
        self.transfoResults=None
        self.cap=None
        self.multiMediapipeWidth = None
        self.image = None
        self.running = False
        th = threading.Thread(target=self.startMultiMediaPipe)
        th.start()


    @abstractmethod
    def execute(self):
        pass

    def startResultLeft(self):
        leftPoseDetector = pose_detector.PoseDetector()
        while self.running:
            if self.image is None:
                continue
            left = self.image.copy()
            cv2.rectangle(left, (self.multiMediapipeWidth-100, 0), (1920, 1080), (0, 0, 0), -1)
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
            cv2.rectangle(right, (0, 0), (self.multiMediapipeWidth + 100, 1080), (0, 0, 0), -1)
            resultsright = rightPoseDetector.detectLandmarks(right)
            if resultsright:
                self.transfoResults[0] = self.manager.wallCalibration.getTransformateLandmarks(resultsright)
        del rightPoseDetector

    def startMultiMediaPipe(self):
        # For webcam input:
        self.cap = Camera(1)
        self.running=True
        self.transfoResults=[None,None]
        thLeft = threading.Thread(target=self.startResultLeft)
        thLeft.start()
        thRight = threading.Thread(target=self.startResultRight)
        thRight.start()
        tmp = np.dot(np.linalg.inv(self.manager.wallCalibration.projectiveMatrix), [[1920//2], [0], [1]])
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
        self.running=False

    def getMultiplePlayerPosition(self):
        playerPosition = [[],[]]
        if self.transfoResults[0]:
            landmark = self.transfoResults[0].landmark
            if -100 <= landmark[15].x * 1920 <= 2100 and -100 <= landmark[15].y * 1080 <= 1200 and -100 <= landmark[17].x * 1920 <= 2100 and -100 <= landmark[17].y * 1080 <= 1200 and -100 <= landmark[19].x * 1920 <= 2100 and -100 <= landmark[19].y * 1080 <= 1200 and -100 <= landmark[21].x * 1920 <= 2100 and -100 <= landmark[21].y * 1080 <= 1200:
                playerPosition[0].append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[15].x * 1920, landmark[15].y * 1080), (landmark[17].x * 1920, landmark[17].y * 1080),(landmark[19].x * 1920, landmark[19].y * 1080), (landmark[21].x * 1920, landmark[21].y * 1080))))

            if -100 <= landmark[16].x * 1920 <= 2100 and -100 <= landmark[16].y * 1080 <= 1200 and -100 <= landmark[18].x * 1920 <= 2100 and -100 <= landmark[18].y * 1080 <= 1200 and -100 <= landmark[20].x * 1920 <= 2100 and -100 <= landmark[20].y * 1080 <= 1200 and -100 <= landmark[22].x * 1920 <= 2100 and -100 <= landmark[22].y * 1080 <= 1200:
                playerPosition[0].append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[16].x * 1920, landmark[16].y * 1080), (landmark[18].x * 1920, landmark[18].y * 1080),(landmark[20].x * 1920, landmark[20].y * 1080), (landmark[22].x * 1920, landmark[22].y * 1080))))

            if -100 <= landmark[27].x * 1920 <= 2100 and -100 <= landmark[27].y * 1080 <= 1200 and -100 <= landmark[29].x * 1920 <= 2100 and -100 <= landmark[29].y * 1080 <= 1200 and -100 <= landmark[31].x * 1920 <= 2100 and -100 <= landmark[31].y * 1080 <= 1200:
                playerPosition[0].append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[27].x * 1920, landmark[27].y * 1080), (landmark[29].x * 1920, landmark[29].y * 1080),(landmark[31].x * 1920, landmark[31].y * 1080))))

            if -100 <= landmark[28].x * 1920 <= 2100 and -100 <= landmark[28].y * 1080 <= 1200 and -100 <= landmark[30].x * 1920 <= 2100 and -100 <= landmark[30].y * 1080 <= 1200 and -100 <= landmark[32].x * 1920 <= 2100 and -100 <= landmark[32].y * 1080 <= 1200:
                playerPosition[0].append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[28].x * 1920, landmark[28].y * 1080), (landmark[30].x * 1920, landmark[30].y * 1080),(landmark[32].x * 1920, landmark[32].y * 1080))))

        if self.transfoResults[1]:
            landmark = self.transfoResults[1].landmark

            if -100 <= landmark[15].x * 1920 <= 2100 and -100 <= landmark[15].y * 1080 <= 1200 and -100 <= landmark[17].x * 1920 <= 2100 and -100 <= landmark[17].y * 1080 <= 1200 and -100 <= landmark[19].x * 1920 <= 2100 and -100 <= landmark[19].y * 1080 <= 1200 and -100 <= landmark[21].x * 1920 <= 2100 and -100 <= landmark[21].y * 1080 <= 1200:
                playerPosition[1].append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[15].x * 1920 , landmark[15].y * 1080), (landmark[17].x * 1920 , landmark[17].y * 1080),(landmark[19].x * 1920 , landmark[19].y * 1080), (landmark[21].x * 1920 , landmark[21].y * 1080))))

            if -100 <= landmark[16].x * 1920 <= 2100 and -100 <= landmark[16].y * 1080 <= 1200 and -100 <= landmark[18].x * 1920 <= 2100 and -100 <= landmark[18].y * 1080 <= 1200 and -100 <= landmark[20].x * 1920 <= 2100 and -100 <= landmark[20].y * 1080 <= 1200 and -100 <= landmark[22].x * 1920 <= 2100 and -100 <= landmark[22].y * 1080 <= 1200:
                playerPosition[1].append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[16].x * 1920 , landmark[16].y * 1080), (landmark[18].x * 1920 , landmark[18].y * 1080),(landmark[20].x * 1920 , landmark[20].y * 1080), (landmark[22].x * 1920 , landmark[22].y * 1080))))

            if -100 <= landmark[27].x * 1920 <= 2100 and -100 <= landmark[27].y * 1080 <= 1200 and -100 <= landmark[29].x * 1920 <= 2100 and -100 <= landmark[29].y * 1080 <= 1200 and -100 <= landmark[31].x * 1920 <= 2100 and -100 <= landmark[31].y * 1080 <= 1200:
                playerPosition[1].append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[27].x * 1920 , landmark[27].y * 1080), (landmark[29].x * 1920 , landmark[29].y * 1080),(landmark[31].x * 1920 , landmark[31].y * 1080))))

            if -100 <= landmark[28].x * 1920 <= 2100 and -100 <= landmark[28].y * 1080 <= 1200 and -100 <= landmark[30].x * 1920 <= 2100 and -100 <= landmark[30].y * 1080 <= 1200 and -100 <= landmark[32].x * 1920 <= 2100 and -100 <= landmark[32].y * 1080 <= 1200:
                playerPosition[1].append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[28].x * 1920 , landmark[28].y * 1080), (landmark[30].x * 1920 , landmark[30].y * 1080),(landmark[32].x * 1920 , landmark[32].y * 1080))))
        return playerPosition