import threading
from abc import abstractmethod
import mediapipe as mp

import cv2
import mediapipe as mp
import numpy as np

import src
from src.controllers.games.game import Game
from src.controllers.switch_frame_controller import SwitchFrameController
from src.model.components.player import Player
from src.utils.camera import Camera
from src.utils.detectors import pose_detector
from src.utils.transform import Transform

mp_pose = mp.solutions.pose


class GameMultiPlayer(Game):

    @abstractmethod
    def __init__(self, parent):
        super().__init__(parent)

        self.player1 = Player(parent)  # left player
        parent.add(self.player1)
        self.player2 = Player(parent)  # right player
        parent.add(self.player2)

        self.player1.pseudo="Joueur 1"
        self.player2.pseudo="Joueur 2"

        self.results = {self.player1: None, self.player2: None}
        self.cap = None
        self.multiMediapipeWidth = None
        self.image = None
        self.continueGame = True

        thMediapipe = threading.Thread(target=self.startMultiMediaPipe)
        thMediapipe.start()
        thPlayer1Position = threading.Thread(target=self.setPlayerPosition, args=[self.player1])
        thPlayer1Position.start()
        thPlayer2Position = threading.Thread(target=self.setPlayerPosition, args=[self.player2])
        thPlayer2Position.start()

    @abstractmethod
    def execute(self):
        pass

    def startResult(self, player, topLeft, bottomRight):
        print(topLeft)
        print(bottomRight)
        poseDetector = pose_detector.PoseDetector()
        while self.continueGame:
            if self.image is None:
                continue
            copy = self.image.copy()
            cv2.rectangle(copy, topLeft, bottomRight, (0, 0, 0), -1)
            results = poseDetector.detectLandmarks(copy)
            if results:
                self.results[player] = results
        del poseDetector

    def startMultiMediaPipe(self):
        # For webcam input:
        self.cap = Camera()

        try:
            tmp = np.dot(np.linalg.inv(Transform().projectiveMatrix), [[self.cap.w // 2], [0], [1]])
        except:
            self.continueGame=False
            SwitchFrameController().execute(frame=src.view.frames.games_frame.GamesFrame)
            return

        self.multiMediapipeWidth = int((tmp[0]//tmp[2])[0])
        print(self.multiMediapipeWidth)

        thLeft = threading.Thread(target=self.startResult, args=[self.player1, (self.multiMediapipeWidth + 60, 0), (int(self.cap.w), int(self.cap.h))])
        thLeft.start()
        thRight = threading.Thread(target=self.startResult, args=[self.player2, (0, 0), (self.multiMediapipeWidth - 60, int(self.cap.h))])
        thRight.start()


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

    def setPlayerPosition(self, player):
        while self.continueGame:
            if self.results[player]:
                landmarks = self.results[player].landmark
                self.setPlayerLandmarks(player, landmarks, mp_pose.PoseLandmark.LEFT_WRIST, 3)
                self.setPlayerLandmarks(player, landmarks, mp_pose.PoseLandmark.RIGHT_WRIST, 3)
                self.setPlayerLandmarks(player, landmarks, mp_pose.PoseLandmark.LEFT_ANKLE, 3)
                self.setPlayerLandmarks(player, landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE, 3)

    def setPlayerLandmarks(self, player, landmarks, root, nbLandmarks):
        valid = True
        ids = range(0, nbLandmarks * 2 - 1, 2)

        if valid:
            # calibrate the landmarks
            moyX = 0
            moyY = 0
            for i in ids:
                moyX += landmarks[root + i].x
                moyY += landmarks[root + i].y

            moyX /= nbLandmarks
            moyY /= nbLandmarks

            tabMoy = [moyX, moyY]

            Transform().getTransformatedPoint(tabMoy)

            player.landmarks[root] = (int(tabMoy[0] * 1920), int(tabMoy[1] * 1080))
