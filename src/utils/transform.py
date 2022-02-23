# TODO: generer (et retourner) une matrice de transformation a partir des 4 coordonnees passees en parametres
import cv2
import numpy as np
import math
from src.utils.Singleton import Singleton

from src.utils.camera import Camera
from src.utils.detectors.surface_detector import Surface


class Transform(metaclass=Singleton):

    def __init__(self):
        self.cam = Camera()
        self.dimCam = [1920, 1080]
        self.projectiveMatrix = None
        self.coordonatesDivider = None
        self.sortedCornerPoints = [[0 for i in range(2)] for y in range(4)]
        self.tab = [[0 for i in range(2)] for y in range(4)]

    def __sortCornerPoints__(self, tabCornerPoints):
        i = 0
        for i in range(4):
            for y in range(2):
                self.tab[i][y] = tabCornerPoints[i][0][y]

        self.sortedCornerPoints[0] = self.__findDistance([0, 0])
        self.sortedCornerPoints[1] = self.__findDistance([self.dimCam[0], 0])
        self.sortedCornerPoints[2] = self.__findDistance([0, self.dimCam[1]])
        self.sortedCornerPoints[3] = self.__findDistance(self.dimCam)

        return self.tab

    def __findDistance(self, cornerPoint):
        minDist = 9000

        for point in self.tab:
            a = (point[0] - cornerPoint[0]) ** 2
            b = (point[1] - cornerPoint[1]) ** 2
            dist = math.sqrt(a + b)
            if (minDist > dist):
                minDist = dist
                minPoint = point
        return minPoint

    def startCalibration(self):
        success, tab = Surface().findCornerPoints()
        if not success:
            print("Calibration failed")
            return False
        print(tab)
        self.__sortCornerPoints__(tab)
        print(self.sortedCornerPoints)
        src_points = np.float32(self.sortedCornerPoints)
        # src_points = np.float32([[62,139],[575,126],[5,424],[634,424]])
        dst_points = np.float32([[0, 0], [self.cam.w, 0], [0, self.cam.h], [self.cam.w, self.cam.h]])
        self.projectiveMatrix = cv2.getPerspectiveTransform(src_points, dst_points)
        # print(self.projectiveMatrix)
        if np.linalg.det(self.projectiveMatrix) == 0:
            print("Determinant de la matrice de transformation = 0 !")
            return False

        return True

    def getTransformateLandmarks(self, tabPoints):
        for point in tabPoints.landmark:
            tmp = np.dot(self.projectiveMatrix, [[point.x * self.cam.w], [point.y * self.cam.h], [1]])
            point.x = (tmp[0] / tmp[2]) / self.cam.w
            point.y = (tmp[1] / tmp[2]) / self.cam.h
        return tabPoints
    def getTransformateKeypoints(self, tabKeyPoints):
        a = []

        for image in tabKeyPoints:
            for point in image:
                tmp = np.dot(self.projectiveMatrix, [[point.pt[0] * 1920], [point.pt[1] * 1080], [1]])
                a.append((tmp[0] / tmp[2]) / 1920)
                a.append((tmp[1] / tmp[2]) / 1080)
                monTuple = (a[0][0], a[1][0])
                point.pt = monTuple

        return tabKeyPoints