import cv2

from src.controllers.utils.camera import Camera
from src.model.components.handle import Handle
from src.model.components.path import Path
from src.model.components.wall import Wall
from src.model.database import Database
#

cam = Camera(0)

while True:
    print("ratio")
    success, img = cam.read()
    if not success:
        continue

    cv2.imshow('camera', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()



