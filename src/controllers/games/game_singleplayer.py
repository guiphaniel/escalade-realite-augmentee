import threading
from abc import abstractmethod
import mediapipe as mp
import cv2

from src.controllers.games.game import Game
from src.model.components.player import Player
from src.utils.camera import Camera
from src.utils.detectors import pose_detector
from src.utils.transform import Transform

mp_pose = mp.solutions.pose

class GameSinglePlayer(Game):

    @abstractmethod
    def __init__(self, parent, player):
        super().__init__(parent)
        self.transfoResults=None
        self.cap=None
        self.multiMediapipeWidth = None
        self.image = None
        self.continueGame = True
        player.parent = parent
        self.player = player
        self.parent.add(self.player)
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

            self.transfoResults = Transform().getTransformateLandmarks(results)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        del singlePoseDetector

    def setPlayerPosition(self):
        while self.continueGame:
            if self.transfoResults:
                landmarks = self.transfoResults.landmark
                self.setPlayerLandmarks(landmarks, mp_pose.PoseLandmark.LEFT_WRIST, 3)
                self.setPlayerLandmarks(landmarks, mp_pose.PoseLandmark.RIGHT_WRIST, 3)
                self.setPlayerLandmarks(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE, 3)
                self.setPlayerLandmarks(landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE, 3)

    def setPlayerLandmarks(self, landmarks, root, nbLandmarks):
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

            self.player.landmarks[root] = (moyX * 1920, moyY * 1080)