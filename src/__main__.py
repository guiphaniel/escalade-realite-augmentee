from src.model.components.handle import Handle
from src.model.components.path import Path
from src.model.components.wall import Wall
from src.model.database import Database
from src.view.manager import Manager
def processMenu():
    disp = Manager(1280,720)
    disp.start()

processMenu()


# database = Database()
# handle1 = Handle(5, 6)
# handle2 = Handle(4, 10)
# handles = [handle1, handle2]
# wall1 = Wall()
# wall2 = Wall("mon super mur")
# database.setWalls([wall1, wall2])
# database.setHandlesInWall(handles, wall1)
# path1 = Path()
# path2 = Path("nom")
# database.setPathsInWall([path1, path2], wall1)
# freePath = Path()
# database.setPathsInWall([freePath, Path(), Path()], None)
# database.setHandlesInPath([handle1], path1)
# database.setHandlesInPath([handle1, handle2], path2)
# database.setHandlesInPath([Handle(5, 4), Handle(1, 7)], freePath)