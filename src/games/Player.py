import numpy as np

class Player:

    def __init__(self,landmarks):
        self.footLeftX = -1
        self.footLeftY = -1
        self.footRightX = -1
        self.footRightY = -1
        self.handLeftX = -1
        self.handLeftY = -1
        self.handRightX = -1
        self.handRightY = -1
        self.landmarks = landmarks

    def setFootLeft(self, x, y):
        self.footLeftX = x
        self.footLeftY = y

    def setFootRight(self, x, y):
        self.footRightX = x
        self.footRightY = y

    def setHandLeft(self, x, y):
        self.handLeftX = x
        self.handLeftY = y

    def setHandRight(self, x, y):
        self.handRightX = x
        self.handRightY = y

    def refresh(self):
        if not self.landmarks:
            return

        self.setHandLeft(self.landmarks.landmark[15].x,self.landmarks.landmark[15].y)
        self.setHandRight(self.landmarks.landmark[16].x,self.landmarks.landmark[16].y)
        self.setFootLeft(self.landmarks.landmark[29].x, self.landmarks.landmark[29].y)
        self.setFootRight(self.landmarks.landmark[30].x, self.landmarks.landmark[30].y)