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

        self.transfoResults = {self.player1: None, self.player2: None}
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
        leftPoseDetector = pose_detector.PoseDetector()
        while self.continueGame:
            if self.image is None:
                continue
            copy = self.image.copy()
            cv2.rectangle(copy, topLeft, bottomRight, (0, 0, 0), -1)
            resultleft = leftPoseDetector.detectLandmarks(copy)
            if resultleft:
                self.transfoResults[player] = Transform().getTransformateLandmarks(resultleft)
        del leftPoseDetector

    def startMultiMediaPipe(self):
        # For webcam input:
        self.cap = Camera()

        try:
            tmp = np.dot(np.linalg.inv(Transform().projectiveMatrix), [[1920 // 2], [0], [1]])
        except:
            #TODO: afficher un popup demandant de recalibrer
            self.continueGame=False
            SwitchFrameController().execute(frame=src.view.frames.games_frame.GamesFrame())
            return

        self.multiMediapipeWidth = int((tmp[0] // tmp[2])[0])

        thLeft = threading.Thread(target=self.startResult, args=[self.player1, (self.multiMediapipeWidth + 30, 0), (1920, 1080)])
        thLeft.start()
        thRight = threading.Thread(target=self.startResult, args=[self.player2, (0, 0), (self.multiMediapipeWidth - 30, 1080)])
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
            if self.transfoResults[player]:
                landmarks = self.transfoResults[player].landmark
                self.setPlayerLandmarks(player, landmarks, mp_pose.PoseLandmark.LEFT_WRIST, 4)
                self.setPlayerLandmarks(player, landmarks, mp_pose.PoseLandmark.RIGHT_WRIST, 4)
                self.setPlayerLandmarks(player, landmarks, mp_pose.PoseLandmark.LEFT_ANKLE, 3)
                self.setPlayerLandmarks(player, landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE, 3)

    def setPlayerLandmarks(self, player, landmarks, root, nbLandmarks):
        valid = True
        ids = range(0, nbLandmarks * 2 - 1, 2)

        # check for the landmarks accuracy (we don't want landmarks that are predicted by mediapipe)
        for i in ids:
            if landmarks[root + i].visibility < 0.15:
                valid = False

        if valid:
            # calibrate the landmarks
            tmpLandmarks = []
            for i in ids:
                l = landmarks[root + i]

                tmpLandmarks.append((l.x * 1920, l.y * 1080))

            # ckeck if the area of the limb isn't too big (else, pygame will freeze)
            if ((max([l[0] for l in tmpLandmarks]) - min([l[0] for l in tmpLandmarks])) * (
                    max([l[1] for l in tmpLandmarks]) - min([l[1] for l in tmpLandmarks])) < 20000) and 0 < (max([l[0] for l in tmpLandmarks]) + min([l[0] for l in tmpLandmarks])) / 2 < 1920 and 0 < (max([l[1] for l in tmpLandmarks]) + min([l[1] for l in tmpLandmarks])) / 2 < 1080:
                #player.mutexes[root].acquire()
                player.landmarks[root] = tmpLandmarks
                #player.mutexes[root].release()
