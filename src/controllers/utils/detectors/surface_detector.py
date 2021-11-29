#TODO: detecter la surface de jeu
import cv2
import numpy as np

class Surface:



    def __findCornerPoints__(self,transform):
        
        cv2.namedWindow('Calibration', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Calibration',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Calibration',cv2.imread("D:/Git/ptut/src/view/images/BlueScreen.png"))
        cv2.waitKey(1000)
        cap = cv2.VideoCapture(0)
        #_, frame = cap.read()
        frame= cv2.imread("D:/bapti/Pictures/Camera Roll/WIN_20211116_14_18_20_Pro.jpg")
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cap.release()
        # Threshold of blue in HSV space
        lower_blue = np.array([60, 35, 140])
        upper_blue = np.array([217, 255, 255])

        # preparing the mask to overlay
        originalImg = cv2.inRange(hsv, lower_blue, upper_blue)

        #filters image bilaterally and displays it
        bilatImg = cv2.bilateralFilter(originalImg, 5, 175, 175)

        #finds edges of bilaterally filtered image and displays it
        edgeImg = cv2.Canny(bilatImg, 75, 200)

        #gets contours (outlines) for shapes and sorts from largest area to smallest area
        contours, hierarchy = cv2.findContours(edgeImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)


        # find the perimeter of the first closed contour
        perim = cv2.arcLength(contours[0], True)
        # setting the precision
        epsilon = 0.02*perim
        # approximating the contour with a polygon
        approxCorners = cv2.approxPolyDP(contours[0], epsilon, True)
        # check how many vertices has the approximate polygon
        approxCornersNumber = len(approxCorners)
        print("Number of approximated corners: ", approxCornersNumber)
        cv2.destroyAllWindows()
        # can also be used to filter before moving on [if needed]
        if approxCornersNumber== 4:
        # printing the position of the calculated corners
            return approxCorners
        else:
            print("Erreur lors de la detection des point ")