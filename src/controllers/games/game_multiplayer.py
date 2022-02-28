import threading
from abc import abstractmethod

import cv2
import numpy as np
import pygame.draw

from src.controllers.games.game import Game
from src.utils.camera import Camera
from src.utils.detectors import pose_detector
from src.utils.transform import Transform


class GameMultiPlayer(Game):

    @abstractmethod
    def __init__(self, parent):
        super().__init__(parent)
        self.transfoResults = None
        self.cap = None
        self.multiMediapipeWidth = None
        self.image = None
        self.continueGame = False
        self.playersPosition = {0:{},1:{}}
        self.playerRadius = 50
        thMediapipe = threading.Thread(target=self.startMultiMediaPipe)
        thMediapipe.start()
        thPlayer1Position = threading.Thread(target=self.setPlayerPosition,args=[0])
        thPlayer1Position.start()
        thPlayer2Position = threading.Thread(target=self.setPlayerPosition,args=[1])
        thPlayer2Position.start()

    @abstractmethod
    def execute(self):
        pass

    def startResultLeft(self):
        leftPoseDetector = pose_detector.PoseDetector()
        while self.continueGame:
            if self.image is None:
                continue
            left = self.image.copy()
            cv2.rectangle(left, (self.multiMediapipeWidth + 100, 0), (1920, 1080), (0, 0, 0), -1)
            resultleft = leftPoseDetector.detectLandmarks(left)
            if resultleft:
                self.transfoResults[0] = Transform().getTransformateLandmarks(resultleft)
        del leftPoseDetector

    def startResultRight(self):
        rightPoseDetector = pose_detector.PoseDetector()
        while self.continueGame:
            if self.image is None:
                continue
            right = self.image.copy()
            cv2.rectangle(right, (0, 0), (self.multiMediapipeWidth - 100, 1080), (0, 0, 0), -1)
            resultsright = rightPoseDetector.detectLandmarks(right)
            if resultsright:
                self.transfoResults[0] = Transform().getTransformateLandmarks(resultsright)
        del rightPoseDetector

    def startMultiMediaPipe(self):
        # For webcam input:
        self.cap = Camera()
        self.continueGame = True
        self.transfoResults = [None, None]
        thLeft = threading.Thread(target=self.startResultLeft)
        thLeft.start()
        thRight = threading.Thread(target=self.startResultRight)
        thRight.start()
        tmp = np.dot(np.linalg.inv(Transform().projectiveMatrix), [[1920 // 2], [0], [1]])
        self.multiMediapipeWidth = int((tmp[0] // tmp[2])[0])

        while self.continueGame:
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
        self.continueGame = False

    def setPlayerPosition(self,playerNumber):
        while self.continueGame:
            if self.transfoResults is None:
                continue
            if self.transfoResults[playerNumber]:
                landmark = self.transfoResults[playerNumber].landmark
                for n in [15, 16]:
                    self.playersPosition[playerNumber][n] = [((landmark[n].x + landmark[n + 2].x + landmark[n + 4].x + landmark[n + 6].x)/4.0)*1920,((landmark[n].y + landmark[n + 2].y + landmark[n + 4].y + landmark[n + 6].y)/4.0)*1080]
                    pygame.draw.circle(self.win,(0,0,255), self.playersPosition[playerNumber][n], self.playerRadius)
                for n in [27, 28]:
                    self.playersPosition[playerNumber][n] = [((landmark[n].x + landmark[n + 2].x + landmark[n + 4].x)/3.0)*1920,((landmark[n].y + landmark[n + 2].y + landmark[n + 4].y)/3.0)*1080]
                    pygame.draw.circle(self.win, (0, 0, 255), self.playersPosition[playerNumber][n], self.playerRadius)

#    def setPlayer2Position(self):
#        while self.continueGame:
#            if self.transfoResults is None:
#                continue
#            if self.transfoResults[1]:
#                landmark = self.transfoResults[1].landmark
#                for n in [15, 16]:
#                    if -100 <= landmark[n].x * 1920 <= 2100 and -100 <= landmark[n].y * 1080 <= 1200 and -100 <= landmark[n + 2].x * 1920 <= 2100 and -100 <= landmark[n + 2].y * 1080 <= 1200 and -100 <= landmark[n + 4].x * 1920 <= 2100 and -100 <= landmark[n + 4].y * 1080 <= 1200 and -100 <= landmark[n + 6].x * 1920 <= 2100 and -100 <= landmark[n + 6].y * 1080 <= 1200:
#                        self.playersPosition[1][n] = (pygame.draw.polygon(self.win, (0, 0, 255), ((landmark[n].x * 1920, landmark[n].y * 1080), (landmark[n + 2].x * 1920, landmark[n + 2].y * 1080),(landmark[n + 4].x * 1920, landmark[n + 4].y * 1080),(landmark[n + 6].x * 1920, landmark[n + 6].y * 1080))))
#
#                for n in [27, 28]:
#                    if -100 <= landmark[n].x * 1920 <= 2100 and -100 <= landmark[n].y * 1080 <= 1200 and -100 <= landmark[n + 2].x * 1920 <= 2100 and -100 <= landmark[n + 2].y * 1080 <= 1200 and -100 <= landmark[n + 4].x * 1920 <= 2100 and -100 <= landmark[n + 4].y * 1080 <= 1200:
#                        self.playersPosition[1][n] = (pygame.draw.polygon(self.win, (0, 0, 255), ((landmark[n].x * 1920, landmark[n].y * 1080), (landmark[n + 2].x * 1920, landmark[n + 2].y * 1080),(landmark[n + 4].x * 1920, landmark[n + 4].y * 1080))))

