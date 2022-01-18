import cv2

from src.controllers.utils.camera import Camera
from src.model.components.handle import Handle
from src.model.components.path import Path
from src.model.components.wall import Wall
from src.model.database import Database
#
cam = Camera(0)

while True:
    
    success, img = cam.read()
    if not success:
        continue

    cv2.namedWindow('camera', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('camera', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('camera', img)



