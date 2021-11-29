#TODO: generer (et retourner) une matrice de transformation a partir des 4 coordonnees passees en parametres
import cv2
import numpy as np

from src.controllers.utils.detectors import surface_detector

class Transform:
    
    def __init__(self):


        self.projectiveMatrix = None
        self.coordonatesDivider = None
        self.sortedCornerPoints =[[0 for i in range(2)]for y in range(4)]    
        self.tab = [[0 for i in range(2)]for y in range(4)]    
            
        

    def __sortCornerPoints__(self, tabCornerPoints):
        i=0
        for i in range(4):
            for y in range(2):
                self.tab[i][y]=tabCornerPoints[i][0][y]
        while i<3:
            if tabCornerPoints[i][0][0]>tabCornerPoints[i+1][0][0]:
                temp=tabCornerPoints[i+1][0]
                tabCornerPoints[i+1][0]=tabCornerPoints[i][0]
                tabCornerPoints[i][0]=temp
                i=0
            else:
                i+=1
        if tabCornerPoints[0][0][1]>tabCornerPoints[1][0][1]:
            self.sortedCornerPoints[0][0]=tabCornerPoints[1][0][0]
            self.sortedCornerPoints[0][1]=tabCornerPoints[1][0][1]
            self.sortedCornerPoints[2][0]=tabCornerPoints[0][0][0]
            self.sortedCornerPoints[2][1]=tabCornerPoints[0][0][1]
        else:
            self.sortedCornerPoints[0][0]=tabCornerPoints[0][0][0]
            self.sortedCornerPoints[0][1]=tabCornerPoints[0][0][1]
            self.sortedCornerPoints[2][0]=tabCornerPoints[1][0][0]
            self.sortedCornerPoints[2][1]=tabCornerPoints[1][0][1]
        if tabCornerPoints[2][0][1]>tabCornerPoints[3][0][1]:
            self.sortedCornerPoints[1][0]=tabCornerPoints[3][0][0]
            self.sortedCornerPoints[1][1]=tabCornerPoints[3][0][1]
            self.sortedCornerPoints[3][0]=tabCornerPoints[2][0][0]
            self.sortedCornerPoints[3][1]=tabCornerPoints[2][0][1]
        else:
            self.sortedCornerPoints[1][0]=tabCornerPoints[2][0][0]
            self.sortedCornerPoints[1][1]=tabCornerPoints[2][0][1]
            self.sortedCornerPoints[3][0]=tabCornerPoints[3][0][0]
            self.sortedCornerPoints[3][1]=tabCornerPoints[3][0][1]
        return self.sortedCornerPoints

    def startCalibration(self):
            tab=surface_detector.Surface.__findCornerPoints__(surface_detector.Surface,self)
            print(tab)
            self.__sortCornerPoints__(tab)
            print(self.sortedCornerPoints)
            src_points = np.float32(self.sortedCornerPoints)
            #src_points = np.float32([[62,139],[575,126],[5,424],[634,424]])
            dst_points = np.float32([[0,0], [640,0], [0,480], [640,480]])
            self.projectiveMatrix= cv2.getPerspectiveTransform(src_points, dst_points)
            print (self.projectiveMatrix)
            print("Calibration réussite") #trop fort

    def getTransformateLandmarks(self, tabPoints):
        for point in tabPoints.landmark:
            
            point.x=point.x*640
            point.y=point.y*480
            self.coordonatesDivider = point.x*self.projectiveMatrix[2][0]+point.y*self.projectiveMatrix[2][1]+self.projectiveMatrix[2][2]
            point.x= point.x*self.projectiveMatrix[0][0]+point.y*self.projectiveMatrix[0][1]+self.projectiveMatrix[0][2]
            point.x= point.x/self.coordonatesDivider
            point.y= point.x*self.projectiveMatrix[1][0]+point.y*self.projectiveMatrix[1][1]+self.projectiveMatrix[1][2]
            point.y=point.y/self.coordonatesDivider
            point.x=point.x/640
            point.y=point.y/480
        return tabPoints

    
   
    
