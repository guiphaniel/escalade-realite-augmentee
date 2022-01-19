#TODO: gestion des joueurs + historique des parties

# assumes that other devs won't put a handle in a path that is not in the same wall than path is
# /!\ est un singleton
import logging
import sqlite3

from absl.app import Error

import src
from src.Singleton import Singleton


class Database(metaclass=Singleton):
    def __init__(self):
        self.logger = logging.getLogger('log')
        try:
            self.con = sqlite3.connect("database.db", isolation_level=None)
        except Error as e:
            print(e)

        self.cur = self.con.cursor()

    def __del__(self):
        self.__closeConnection()

    def __getWallsIdsInDb(self):
        self.cur.execute("select id from walls")
        return [id[0] for id in self.cur.fetchall()]

    def __getPathsIdsInDb(self):
        self.cur.execute("select id from paths")
        return [id[0] for id in self.cur.fetchall()]

    def __getHandlesIdsInDb(self):
        self.cur.execute("select id from handles")
        return [id[0] for id in self.cur.fetchall()]

    def __getPlayersIdsInDb(self):
        self.cur.execute("select id from players")
        return [id[0] for id in self.cur.fetchall()]

    def setWalls(self, walls):
        DbWallsIds = self.__getWallsIdsInDb()

        # add/update new/changed walls
        for wall in walls:
            if wall.id not in DbWallsIds:
                self.__addWall(wall)
            else:
                self.__updateWall(wall)

        # remove all walls that were previously in the db and that are no longer needed
        wallsIds = [wall.id for wall in walls if wall.id]

        wallsToRemove = [id for id in DbWallsIds if id not in wallsIds]

        for id in wallsToRemove:
            self.cur.execute("delete from walls where id=:id", {"id": id})

    def __addWall(self, wall):
        # insert
        self.cur.execute("insert into walls values(null, :name)",
                    {"name": wall.name})
        wall.id = self.cur.lastrowid

        # set default name
        if not wall.name:
            wall.name = "Mur " + str(wall.id)
            self.cur.execute("update walls set name=:name where id=:id",
                        {"name": wall.name, "id": wall.id})

    def __updateWall(self, wall):
        # update
        self.cur.execute("update walls set name=:name where id=:id",
                    {"name": wall.name, "id":wall.id})

    def getWalls(self):
        self.cur.execute("select * from walls")

        result = self.cur.fetchall()

        walls = []
        for w in result:
            wall = src.model.components.wall.Wall(w[1])
            wall.id = w[0]
            walls.append(wall)

        return walls

    def getHandlesInWall(self, wall):
        # if the wall doesn't exist yet, warning
        if not wall.id:
            self.logger.warning("wall hasn't been initialized", stack_info=True)

        self.cur.execute("select * from handles where wallId=:wallId",
                    {"wallId": wall.id})

        result = self.cur.fetchall()

        handles = []
        for h in result:
            handle = src.model.components.handle.Handle(h[1], h[2])
            handle.id = h[0]
            handles.append(handle)

        return handles

    def setHandlesInWall(self, handles, wall):
        if wall.id not in self.__getWallsIdsInDb():
            self.logger.warning("wall hasn't been initialized", stack_info=True)
            return

        handlesIdsInDb = self.__getHandlesIdsInDb()

        # add/update new/changed handles
        for handle in handles:
            if handle.id not in handlesIdsInDb:
                self.__addHandleInWall(handle, wall)
            else:
                self.__updateHandleInWall(handle, wall)

        # remove all handles that were previously in the db and that are no longer needed
        handlesIds = [handle.id for handle in handles]

        handlesToRemove = [id for id in handlesIdsInDb if id not in handlesIds]

        for id in handlesToRemove:
            self.cur.execute("delete from handles where id=:id", {"id": id})

    def __addHandleInWall(self, handle, wall):
        self.cur.execute("insert into handles values(null, :x, :y, :wallId)",
                    {"x": handle.x, "y": handle.y, "wallId": wall.id})
        handle.id = self.cur.lastrowid

    def __updateHandleInWall(self, handle):
        self.cur.execute("update handles set x=:x, y=:y where id=:id", {"x": handle.x, "y": handle.y, "id": handle.id})

    def setPathsInWall(self, paths, wall):
        if wall.id not in self.__getWallsIdsInDb():
            self.logger.warning("wall hasn't been initialized", stack_info=True)
            return

        pathsIdsInDb = self.__getPathsIdsInDb()

        # remove all paths that were previously in the db and that are no longer needed
        pathsIds = [path.id for path in paths if path.id]

        pathsToRemove = [id for id in pathsIdsInDb if id not in pathsIds]

        for id in pathsToRemove:
            self.cur.execute("delete from paths where id=:id", {"id": id})
            self.cur.execute("delete from pathsHandles where pathId=:pathId", {"pathId": id}) #must do that because on delete cascade doesn't work with python

        # add/update new/changed paths
        for path in paths:
            if path.id not in pathsIdsInDb:
                self.__addPathInWall(path, wall)
            else:
                self.__updatePathInWall(path, wall)

    def __addPathInWall(self, path, wall):
        self.cur.execute("insert into paths values(null, :name, :wallId)",
                    {"name": path.name, "wallId": wall.id})
        path.id = self.cur.lastrowid

        # set default name
        if not path.name:
            path.name = "Parcours " + str(path.id)
            self.cur.execute("update paths set name=:name where id=:id",
                        {"name": path.name, "id": path.id})

    def __updatePathInWall(self, path):
        self.cur.execute("update paths set name=:name where id=:id", {"name": path.name})

    def getPathInWall(self, wall):
        # if the wall doesn't exist yet, warning
        if wall.id not in self.__getWallsIdsInDb():
            self.logger.warning("wall hasn't been initialized", stack_info=True)

        self.cur.execute("select id, name from paths where wallId=:wallId",
                    {"wallId": wall.id})

        result = self.cur.fetchall()

        paths = []
        for p in result:
            path = src.model.components.path.Path(p[1])
            path.id = p[0]
            paths.append(path)

        return paths

    def setHandlesInPath(self, handles, path):
        # if the path doesn't exist yet, warning
        if path.id not in self.__getPathsIdsInDb():
            self.logger.warning("path hasn't been initialized", stack_info=True)
            return

        # TODO: verifier que les wallid des prises sont bien egaux au wallid du path, sinon, error

        handlesIds = [handle.id for handle in handles]

        self.cur.execute("select handleId from pathsHandles where pathId=:pathId",
                    {"pathId": path.id})
        handlesIdsInDb = [id[0] for id in self.cur.fetchall()]

        # add handle to wall in db if it does not exist yet (random point)
        for handle in handles:
            if handle.id not in self.__getHandlesIdsInDb():
                # get wall id of the path
                self.cur.execute("select wallId from paths where id=:id",
                            {"id": path.id})
                wall = src.model.components.wall.Wall()
                wall.id = self.cur.fetchone()[0]

                self.__addHandleInWall(handle, wall)

        # add new handles to path
        handlesToAdd = [id for id in handlesIds if id not in handlesIdsInDb]
        rank = 0
        for handle in handlesToAdd:
            self.__addHandleInPath(handle, path, rank)
            rank = rank + 1

        # update changed handles in path
        handlesToUpdate = [handle for handle in handles if handle.id in handlesIdsInDb]
        rank = 0
        for handle in handlesToUpdate:
            self.__updateHandleInPath(handle, path, rank)
            rank = rank + 1

        # remove all handles from path that were previously in the db and that are no longer needed
        handlesToRemove = [id for id in handlesIdsInDb if id not in handlesIds]

        for id in handlesToRemove:
            self.cur.execute("delete from pathsHandles where pathId=:pathId and handleId=:handleId",
                             {"pathId": path.id, "handleId": id})

    def __addHandleInPath(self, handleId, path, rank: int):
        self.cur.execute("insert into pathsHandles values(:pathId, :handleId, :rank)",
                    {"pathId": path.id, "handleId": handleId, "rank": rank})

    def __updateHandleInPath(self, handle, path, rank):
        self.cur.execute("update handles set x=:x, y=:y where id=:id", {"x": handle.x, "y": handle.y, "id": handle.id})
        self.cur.execute("update pathsHandles set rank=:rank where pathId=:pathId and handleId=:handleId",
                    {"rank": rank, "pathId": path.id, "handleId": handle.id})

    def getHandlesInPath(self, path):
        if path.id not in self.__getPathsIdsInDb():
            self.logger.warning("path hasn't been initialized", stack_info=True)
            return

        self.cur.execute("select handleId, x, y from pathsHandles as ph inner join handles as h on h.id = ph.handleId where pathId = :pathId order by rank",
                    {"pathId": path.id})

        result = self.cur.fetchall()

        handles = []
        for h in result:
            handle = src.model.components.handle.Handle(h[1], h[2])
            handle.id = h[0]
            handles.append(handle)

        return handles

    def setPlayers(self, players):
        DbPlayersIds = self.__getPlayersIdsInDb()

        # add/update new/changed players
        for player in players:
            if player.id not in DbPlayersIds:
                self.__addPlayer(player)
            else:
                self.__updatePlayer(player)

        # remove all players that were previously in the db and that are no longer needed
        playersIds = [player.id for player in players if player.id]

        playersToRemove = [id for id in DbPlayersIds if id not in playersIds]

        for id in playersToRemove:
            self.cur.execute("delete from players where id=:id", {"id": id})

    def __addPlayer(self, player):
        # insert
        self.cur.execute("insert into players values(null, :pseudo)",
                    {"pseudo": player.pseudo})
        player.id = self.cur.lastrowid

        # set default pseudo
        if not player.pseudo:
            player.pseudo = "Joueur " + str(player.id)
            self.cur.execute("update players set pseudo=:pseudo where id=:id",
                        {"pseudo": player.pseudo, "id": player.id})

    def __updatePlayer(self, player):
        # update
        self.cur.execute("update players set pseudo=:pseudo where id=:id",
                    {"pseudo": player.pseudo, "id":player.id})

    def getPlayers(self):
        self.cur.execute("select * from players")

        result = self.cur.fetchall()

        players = []
        for p in result:
            player = src.model.components.player.Player(p[1])
            player.id = p[0]
            players.append(player)

        return players

    def __closeConnection(self):
        self.con.close()
