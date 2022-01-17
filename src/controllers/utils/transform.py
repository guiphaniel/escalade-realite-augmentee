# TODO: generer (et retourner) une matrice de transformation a partir des 4 coordonnees passees en parametres
import cv2
import numpy as np
import math
from src.controllers.utils.detectors import surface_detector


class Transform:

    def __init__(self):

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
        tab = surface_detector.Surface.__findCornerPoints__(surface_detector.Surface, self)
        print(tab)
        self.__sortCornerPoints__(tab)
        print(self.sortedCornerPoints)
        src_points = np.float32(self.sortedCornerPoints)
        # src_points = np.float32([[62,139],[575,126],[5,424],[634,424]])
        dst_points = np.float32([[0, 0], [1920, 0], [0, 1080], [1920, 1080]])
        self.projectiveMatrix = cv2.getPerspectiveTransform(src_points, dst_points)
        print(self.projectiveMatrix)
        print("Calibration rÃ©ussite")  # trop fort

    def getTransformateLandmarks(self, tabPoints):
        for point in tabPoints.landmark:
            tmp = np.dot(self.projectiveMatrix, [[point.x * 1920], [point.y * 1080], [1]])
            point.x = (tmp[0] / tmp[2]) / 1920
            point.y = (tmp[1] / tmp[2]) / 1080
        return tabPoints
