import cv2

from src.controllers.utils.camera import Camera
from src.model.components.handle import Handle
from src.model.components.path import Path
from src.model.components.wall import Wall
from src.model.database import Database
from src.model.database import Database
from src.view.manager import Manager

def processMenu():
    disp = Manager(1920,1080)
    disp.start()

processMenu()


