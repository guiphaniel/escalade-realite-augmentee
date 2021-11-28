#stocke les informations du joueur(nom, points, coordonnees...)

import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

class Player:
    #static variables
    id = 0
    
    # Initializing
    def __init__(self, pseudo):        
        self.id = Player.id
        Player.id += 1
        self.pseudo = pseudo
        
    def getId(self):
        return self.id
    
    def getPseudo(self):
        return self.pseudo
    
    def setPseudo(self, pseudo):
        self.pseudo = pseudo
    
    




