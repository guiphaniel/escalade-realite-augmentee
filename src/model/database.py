#TODO: communique avec la base de donnees. Recupere toutes les donnees au lancement,
# et enregistre quand necessaire (scores en fin de partie, creation de nouveaux murs, parcours, joueurs...)
# contient une liste de murs
# /!\ est un singloton
from src.Singleton import Singleton


class Database(Singleton):
    def importData(self):
        pass

    def insert(self, obj, values):
        objType = type(obj).__name__
        print(objType)
        pass

    def update(self, obj, values):
        pass

    def save(self, obj):
        pass
