import cv2
import mediapipe as mp
import numpy as np
from src.model.components.player import Player
import copy
from src.controllers.utils.detectors import pose_detector
from src.controllers.utils.transform import Transform
from src.model.database import Database
from src.view.manager import Manager


def processMenu():
    disp = Manager(1920,1080)
    disp.start()

processMenu()

database = Database()
database.insert("string", "value")

#wallCalibration = Transform()
#wallCalibration.startCalibration()

