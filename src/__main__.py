from src.model.components.handle import Handle
from src.model.components.wall import Wall
from src.model.database import Database

database = Database()
handle1 = Handle(5, 6)
handle2 = Handle(4, 10)
handles = [handle1, handle2]
wall = Wall()
database.addWall(wall)
database.setHandlesInWall(handles, wall)

