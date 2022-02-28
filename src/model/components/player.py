# stocke les informations du joueur(nom, points, coordonnees...)
import threading

import mediapipe as mp
import pygame
from mediapipe.framework.formats import landmark_pb2

from src.view.items.drawable import Drawable

mp_pose = mp.solutions.pose


class Player(Drawable):

    # Initializing
    def __init__(self, parent, pseudo=None):
        Drawable.__init__(self, parent)
        self.id = None
        self.pseudo = pseudo
        self.limbsRadius = {mp_pose.PoseLandmark.LEFT_WRIST: 50,
                            mp_pose.PoseLandmark.RIGHT_WRIST: 50,
                            mp_pose.PoseLandmark.LEFT_ANKLE: 50,
                            mp_pose.PoseLandmark.RIGHT_ANKLE: 50}

        self.landmarks = {mp_pose.PoseLandmark.LEFT_WRIST: None,
                          mp_pose.PoseLandmark.RIGHT_WRIST: None,
                          mp_pose.PoseLandmark.LEFT_ANKLE: None,
                          mp_pose.PoseLandmark.RIGHT_ANKLE: None}

        self.mutexes = {mp_pose.PoseLandmark.LEFT_WRIST: threading.Lock(),
                        mp_pose.PoseLandmark.RIGHT_WRIST: threading.Lock(),
                        mp_pose.PoseLandmark.LEFT_ANKLE: threading.Lock(),
                        mp_pose.PoseLandmark.RIGHT_ANKLE: threading.Lock()}

    def draw(self):
        self.__drawLimb(mp_pose.PoseLandmark.LEFT_WRIST)
        self.__drawLimb(mp_pose.PoseLandmark.RIGHT_WRIST)
        self.__drawLimb(mp_pose.PoseLandmark.LEFT_ANKLE)
        self.__drawLimb(mp_pose.PoseLandmark.RIGHT_ANKLE)

    def __drawLimb(self, id):
        l = self.landmarks[id]
        r = self.limbsRadius[id]

        if l and r:
            pygame.draw.circle(self.win,(0,0,255), l, r)

    def toString(self):
        return self.name
