from unittest import result
import cv2
import numpy as np


class Handle_Detector:
    
    def __init__(self):
        self.cap = None
        self.img = None
        self.tabKeyPoints = []
        
    def startHandleDetector(self, manager):
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        success = False
        while (success == False):
            success, self.img = self.cap.read()
        self.findTabKeyPoints(manager)
        self.cap.release()


    def findTabKeyPoints(self, manager):
        rows, cols, ch = self.img.shape

        self.img = cv2.warpPerspective(self.img, manager.wallCalibration.projectiveMatrix, (cols, rows))

        params = cv2.SimpleBlobDetector_Params()
        params.minThreshold = 1
        params.maxThreshold = 255
        params.filterByArea = True
        params.filterByColor = False
        params.filterByCircularity = False
        params.filterByConvexity = False
        params.filterByInertia = False

        for i in [10,30,50,80,100,200,400]:
            params.minArea = i
            params.maxArea = i*10
            detector = cv2.SimpleBlobDetector_create(params)
        # Detect blobs.
            keypoints = detector.detect(self.img)
            # Affichage :
            #im_with_keypoints = cv2.drawKeypoints(self.img, keypoints, np.array([]), (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            #cv2.imshow('frame'+str(i), im_with_keypoints)
            self.tabKeyPoints.append(keypoints)
        return self.tabKeyPoints

    