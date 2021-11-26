from numpy import sqrt

class PoseDetector:
    
    def detectCollision(self, point1, radius1, point2, radius2):
        return sqrt(pow(point1.x-point2.x, 2) + pow(point1.y-point2.y, 2)) <= radius1 + radius2

