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
    def __init__(self,manager):
        self.manager=manager
        self.transfoResults=None
        self.cap=None
        self.multiMediapipeWidth = None
        self.image = None
        self.running = False
        self.playerPosition = {}
        thMediapipe = threading.Thread(target=self.startSingleMediaPipe)
        thMediapipe.start()
        thPlayerPosition = threading.Thread(target=self.setPlayerPosition)
        thPlayerPosition.start()


    @abstractmethod
    def execute(self):
        pass

    def startSingleMediaPipe(self):
        # For webcam input:
        self.cap = Camera()
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

    def setPlayerPosition(self):
        while self.running:
            if self.transfoResults:
                landmark = self.transfoResults.landmark
                for n in [15,16]:
                    if -100<=landmark[n].x * 1920<=2100 and -100<=landmark[n].y * 1080<=1200 and -100<=landmark[n+2].x * 1920<=2100 and -100<=landmark[n+2].y * 1080<=1200 and -100<=landmark[n+4].x * 1920<=2100 and -100<=landmark[n+4].y * 1080<=1200 and -100<=landmark[n+6].x * 1920<=2100 and -100<=landmark[n+6].y * 1080<=1200 :
                        self.playerPosition[n]=(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[n].x * 1920, landmark[n].y * 1080), (landmark[n+2].x * 1920, landmark[n+2].y * 1080),(landmark[n+4].x * 1920, landmark[n+4].y * 1080),(landmark[n+6].x * 1920, landmark[n+6].y * 1080))))

                for n in [27,28]:
                    if -100<=landmark[n].x * 1920<=2100 and -100<=landmark[n].y * 1080<=1200 and -100<=landmark[n+2].x * 1920<=2100 and -100<=landmark[n+2].y * 1080<=1200 and -100<=landmark[n+4].x * 1920<=2100 and -100<=landmark[n+4].y * 1080<=1200 :
                        self.playerPosition[n]=(pygame.draw.polygon(self.manager.screen, (0, 0, 255), ((landmark[n].x * 1920, landmark[n].y * 1080), (landmark[n+2].x * 1920, landmark[n+2].y * 1080),(landmark[n+4].x * 1920, landmark[n+4].y * 1080))))

