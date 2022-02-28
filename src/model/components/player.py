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

        self.landmarks = {mp_pose.PoseLandmark.LEFT_WRIST: [],
                          mp_pose.PoseLandmark.RIGHT_WRIST: [],
                          mp_pose.PoseLandmark.LEFT_ANKLE: [],
                          mp_pose.PoseLandmark.RIGHT_ANKLE: []}

        self.mutexes = {mp_pose.PoseLandmark.LEFT_WRIST: threading.Lock(),
                        mp_pose.PoseLandmark.RIGHT_WRIST: threading.Lock(),
                        mp_pose.PoseLandmark.LEFT_ANKLE: threading.Lock(),
                        mp_pose.PoseLandmark.RIGHT_ANKLE: threading.Lock()}

        self.limbs = {}

    def draw(self):
        self.limbs[mp_pose.PoseLandmark.LEFT_WRIST] = self.__drawLimb(mp_pose.PoseLandmark.LEFT_WRIST)
        self.limbs[mp_pose.PoseLandmark.RIGHT_WRIST] = self.__drawLimb(mp_pose.PoseLandmark.RIGHT_WRIST)
        self.limbs[mp_pose.PoseLandmark.LEFT_ANKLE] = self.__drawLimb(mp_pose.PoseLandmark.LEFT_ANKLE)
        self.limbs[mp_pose.PoseLandmark.RIGHT_ANKLE] = self.__drawLimb(mp_pose.PoseLandmark.RIGHT_ANKLE)


    def __drawLimb(self, id):
        #self.mutexes[id].acquire()
        ls = self.landmarks[id]

        limb = None
        if ls:
            limb = pygame.draw.polygon(self.win, (0, 0, 255), ls)
        #self.mutexes[id].release()

        return limb


    def toString(self):
        return self.name