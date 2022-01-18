# TODO: communique avec la base de donnees. Recupere toutes les donnees au lancement,
# et enregistre quand necessaire (scores en fin de partie, creation de nouveaux murs, parcours, joueurs...)
# contient une liste de murs
# /!\ est un singloton
import logging
import sqlite3

from absl.app import Error

import src
from src.Singleton import Singleton
from src.model.components.handle import Handle
from src.model.components.path import Path


class Database(Singleton):
    def __init__(self):
        self.logger = logging.getLogger('log')
        try:
            self.con = sqlite3.connect("database.db", isolation_level=None)
        except Error as e:
            print(e)

    def __del__(self):
        self.__closeConnection()

    # TODO: convert to setWallForUser()
    def addWall(self, wall):
        # check
        if wall.id:
            self.logger.warning("wall hasn't been initialized", stack_info=True)
            return

        # insert
        cur = self.con.cursor()
        cur.execute("insert into walls values(null, :name)",
                    {"name": wall.name})
        wall.id = cur.lastrowid

        # set default name
        if not wall.name:
            wall.name = "Mur " + str(wall.id)
            cur.execute("update walls set name=:name where id=:id",
                        {"name": wall.name, "id": wall.id})

    # TODO: convert to updateWallForUser()
    def updateWall(self, wall):
        # check
        if not wall.id:
            self.logger.warning("wall hasn't been initialized", stack_info=True)
            return

        # update
        cur = self.con.cursor()
        cur.execute("update walls set name=:name where id=:id",
                    {"name": wall.name, "id":wall.id})
        wall.id = cur.lastrowid

    def getWalls(self):
        cur = self.con.cursor()
        cur.execute("select * from walls")

        result = cur.fetchall()

        walls = []
        for w in result:
            wall = src.model.components.wall.Wall(w[1])
            wall.id = w[0]
            walls.append(wall)

        return walls

    def setHandlesInWall(self, handles: [Handle], wall):
        if not wall.id:
            self.logger.warning("wall hasn't been initialized", stack_info=True)
            return

        # remove all handles that were previously in the db and that are no longer needed
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
                self.__addHandleInWall(handle, wall)
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

    def setPathInWall(self, paths: [Path], wall):
        if not wall.id:
            self.logger.warning("wall hasn't been initialized", stack_info=True)
            return

        # remove all paths that were previously in the db and that are no longer needed
        pathsIds = [path.id for path in paths if path.id]
        cur = self.con.cursor()
        cur.execute("select id from paths where wallId=:wallId",
                    {"wallId": wall.id})
        DbPathsIds = cur.fetchall()

        pathsToRemove = [id[0] for id in DbPathsIds if id[0] not in pathsIds]

        for id in pathsToRemove:
            cur.execute("delete from paths where id=:id", {"id": id})

        # add/update new/changed paths
        for path in paths:
            if not path.id:
                self.__addPathInWall(path, wall)
            else:
                self.__updatePathInWall(path, wall)

    def __addPathInWall(self, path: Path, wall):
        cur = self.con.cursor()
        cur.execute("insert into paths values(null, :name, :wallId)",
                    {"name": path.name, "wallId": wall.id})
        path.id = cur.lastrowid

        # set default name
        if not path.name:
            path.name = "Parcours " + str(path.id)
            cur.execute("update paths set name=:name where id=:id",
                        {"name": path.name, "id": path.id})

    def __updatePathInWall(self, path):
        cur = self.con.cursor()
        cur.execute("update paths set name=:name where id=:id", {"name": path.name})

    def getPathInWall(self, wall):
        # if the wall doesn't exist yet, warning
        if not wall.id:
            self.logger.warning("wall hasn't been initialized", stack_info=True)

        cur = self.con.cursor()
        cur.execute("select id, name from paths where wallId=:wallId",
                    {"wallId": wall.id})

        result = cur.fetchall()

        paths = []
        for p in result:
            path = Path(p[1])
            path.id = p[0]
            paths.append(path)

        return paths

    def setHandleInPath(self, handles: [Handle], path: Path):
        # if the path doesn't exist yet, warning
        if not path.id:
            self.logger.warning("path hasn't been initialized", stack_info=True)
            return

        # initialize cursor
        cur = self.con.cursor()

        # add handle to wall in db if it does not exist yet (random point)
        for handle in handles:
            if not handle.id:
                # get wall id of the path
                cur.execute("select wallId from paths where id=:id",
                            {"id": path.id})
                wall = wall.Wall()
                wall.id = cur.fetchone()[0]

                self.__addHandleInWall(handle, wall)

        # remove all handles from path that were previously in the db and that are no longer needed
        handlesIds = [handle.id for handle in handles]
        cur = self.con.cursor()
        cur.execute("select handleId from pathsHandles where pathId=:pathId",
                    {"pathId": path.id})
        DbHandlesIds = [id[0] for id in cur.fetchall()]

        handlesToRemove = [id for id in DbHandlesIds if id not in handlesIds]

        for id in handlesToRemove:
            cur.execute("delete from pathsHandles where pathId=:pathId and handleId=:handleId", {"pathId": path.id, "handleId": id})

        # add new handles to path
        handlesToAdd = [id for id in handlesIds if id not in DbHandlesIds]
        rank = 0
        for handle in handlesToAdd:
            self.__addHandleInPath(handle, path, rank)
            rank = rank + 1

        # update changed handles in path
        handlesToUpdate = [id for id in DbHandlesIds if id in handlesIds]
        rank = 0
        for handle in handlesToUpdate:
            self.__updateHandleInPath(handle, path, rank)
            rank = rank + 1

    def __addHandleInPath(self, handleId, path, rank: int):
        cur = self.con.cursor()
        cur.execute("insert into pathsHandles values(:pathId, :handleId, :rank)",
                    {"pathId": path.id, "handleId": handleId, "rank": rank})

    def __updateHandleInPath(self, handle: Handle, path: Path, rank):
        cur = self.con.cursor()
        cur.execute("update handles set x=:x, y=:y where id=:id", {"x": handle.x, "y": handle.y, "id": handle.id})
        cur.execute("update pathsHandles set rank=:rank where pathId=:pathId and handleId=:HandleId",
                    {"rank": rank, "pathId": path.id})

    def getHandlesInPath(self, path):
        if not path.id:
            self.logger.warning("path hasn't been initialized", stack_info=True)
            return

        cur = self.con.cursor()
        cur.execute("select handleId, x, y from pathsHandles as ph inner join handles as h on h.id = ph.handleId where pathId = :pathId order by rank",
                    {"pathId": path.id})

        result = cur.fetchall()

        handles = []
        for h in result:
            handle = Handle(h[1], h[2])
            handle.id = h[0]
            handles.append(handle)

        return handles

    def __closeConnection(self):
        self.con.close()
