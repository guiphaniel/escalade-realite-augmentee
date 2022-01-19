# stocke les informations du joueur(nom, points, coordonnees...)

import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2


class Player:

    # Initializing
    def __init__(self, pseudo=None):
        self.id = None
        self.pseudo = pseudo
