from src.model.components.handle import Handle
from src.model.components.path import Path
from src.model.components.wall import Wall
from src.model.database import Database
#
database = Database()
handle1 = Handle(5, 6)
handle2 = Handle(4, 10)
handles = [handle1, handle2]
wall1 = Wall()
wall2 = Wall("mon super mur")
database.setWalls([wall1, wall2])
database.setHandlesInWall(handles, wall1)
path1 = Path()
path2 = Path("nom")
database.setPathsInWall([path1, path2], wall1)
database.setHandlesInPath([handle1], path1)
database.setHandlesInPath([handle1, handle2], path2)

# walls = Database().getWalls()
#
# for wall in walls:
#     print("wall")
#     print(wall.id)
#     paths = Database().getPathInWall(wall)
#
#     for path in paths:
#         print('\t path')
#         print('\t' + str(path.id))
#         handles = Database().getHandlesInPath(path)
#         for handle in handles:
#             print("\t\t handle")
#             print('\t\t' + str(handle.id))


