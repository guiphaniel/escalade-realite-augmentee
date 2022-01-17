# TODO: communique avec la base de donnees. Recupere toutes les donnees au lancement,
# et enregistre quand necessaire (scores en fin de partie, creation de nouveaux murs, parcours, joueurs...)
# contient une liste de murs
# /!\ est un singloton
import logging
import sqlite3

from absl.app import Error

from src.model.components.handle import Handle

from src.Singleton import Singleton
from src.model.components.path import Path
from src.model.components import wall


class Database(Singleton):
    def __init__(self):
        self.logger = logging.getLogger('log')
        try:
            self.con = sqlite3.connect("database.db", isolation_level=None)
        except Error as e:
            print(e)

    def __del__(self):
        self.__closeConnection()

    def setHandlesInWall(self, handles: [Handle], wall):
        if not wall.id:
            self.logger.warning("wall hasn't been initialized", stack_info=True)
            return

        #remove all handles that were previously in the db and that are no longer needed
        handlesIds = [handle.id for handle in handles if handle.id]
        cur = self.con.cursor()
        cur.execute("select id from handles where wallId=:wallId",
                                         {"wallId": wall.id})
        DbHandlesIds = cur.fetchall()

        handlesToRemove = [id[0] for id in DbHandlesIds if id[0] not in handlesIds]

        for id in handlesToRemove:
            cur.execute("delete from handles where id=:id", {"id": id})

        # add/update new/changed handles
        for handle in handles:
            if not handle.id:
                self.__addHandleToWall(handle, wall)
            else:
                self.__updateHandleInWall(handle, wall)

    def getHandlesInWall(self, wall):
        # if the wall doesn't exist yet, warning
        if not wall.id:
            self.logger.warning("wall hasn't been initialized", stack_info=True)

        cur = self.con.cursor()
        cur.execute("select * from handles where wallId=:wallId",
                    {"wallId": wall.id})

        result = cur.fetchall()

        handles = []
        for h in result:
            handle = Handle(h[1], h[2])
            handle.id = h[0]
            handles.append(handle)

        return handles

    def __addHandleInWall(self, handle: Handle, wall):
        cur = self.con.cursor()
        cur.execute("insert into handles values(null, :x, :y, :wallId)",
                    {"x": handle.x, "y": handle.y, "wallId": wall.id})
        handle.id = cur.lastrowid

    def __updateHandleInWall(self, handle):
        cur = self.con.cursor()
        cur.execute("update handles set x=:x, y=:y where id=:id", {"x": handle.x, "y": handle.y, "id": handle.id})

    def __closeConnection(self):
        self.con.close()
