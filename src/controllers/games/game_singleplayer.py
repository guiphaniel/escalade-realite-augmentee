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



class GameSinglePlayer:

    @abstractmethod
    def __init__(self,manager,nbMediaPipe):
        self.manager=manager
        self.transfoResults=None
        self.cap=None
        self.multiMediapipeWidth = None
        self.image = None
        self.running = False
        th = threading.Thread(target=self.startSingleMediaPipe)
        th.start()


    @abstractmethod
    def execute(self):
        pass

    def startSingleMediaPipe(self):
        # For webcam input:
        self.cap = Camera(1)
        self.running=True

        singlePoseDetector = pose_detector.PoseDetector()

        while self.running:
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
        self.running=False

    def getPlayerPosition(self):
        playerPosition = []
        if self.transfoResults:
            landmark = self.transfoResults.landmark
            if -100<=landmark[15].x * 1920<=2100 and -100<=landmark[15].y * 1080<=1200 and -100<=landmark[17].x * 1920<=2100 and -100<=landmark[17].y * 1080<=1200 and -100<=landmark[19].x * 1920<=2100 and -100<=landmark[19].y * 1080<=1200 and -100<=landmark[21].x * 1920<=2100 and -100<=landmark[21].y * 1080<=1200 :
                playerPosition.append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[15].x * 1920, landmark[15].y * 1080), (landmark[17].x * 1920, landmark[17].y * 1080),(landmark[19].x * 1920, landmark[19].y * 1080),(landmark[21].x * 1920, landmark[21].y * 1080))))

            if -100 <= landmark[16].x * 1920 <= 2100 and -100 <= landmark[16].y * 1080 <= 1200 and -100 <= landmark[18].x * 1920 <= 2100 and -100 <= landmark[18].y * 1080 <= 1200 and -100 <= landmark[20].x * 1920 <= 2100 and -100 <= landmark[20].y * 1080 <= 1200 and -100<=landmark[22].x * 1920<=2100 and -100<=landmark[22].y * 1080<=1200 :
                playerPosition.append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[16].x * 1920, landmark[16].y * 1080), (landmark[18].x * 1920, landmark[18].y * 1080),(landmark[20].x * 1920, landmark[20].y * 1080),(landmark[22].x * 1920, landmark[22].y * 1080))))

            if -100 <= landmark[27].x * 1920 <= 2100 and -100 <= landmark[27].y * 1080 <= 1200 and -100 <= landmark[29].x * 1920 <= 2100 and -100 <= landmark[29].y * 1080 <= 1200 and -100 <= landmark[31].x * 1920 <= 2100 and -100 <= landmark[31].y * 1080 <= 1200:
                playerPosition.append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[27].x * 1920, landmark[27].y * 1080), (landmark[29].x * 1920, landmark[29].y * 1080),(landmark[31].x * 1920, landmark[31].y * 1080))))

            if -100 <= landmark[28].x * 1920 <= 2100 and -100 <= landmark[28].y * 1080 <= 1200 and -100 <= landmark[30].x * 1920 <= 2100 and -100 <= landmark[30].y * 1080 <= 1200 and -100 <= landmark[32].x * 1920 <= 2100 and -100 <= landmark[32].y * 1080 <= 1200:
                playerPosition.append(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[28].x * 1920, landmark[28].y * 1080), (landmark[30].x * 1920, landmark[30].y * 1080),(landmark[32].x * 1920, landmark[32].y * 1080))))
        return playerPosition
