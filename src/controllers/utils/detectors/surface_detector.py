#TODO: detecter la surface de jeu
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
class Surface:



    def __findCornerPoints__(self,transform):
        MIN_MATCH_COUNT = 10

        cap = cv.VideoCapture(0)
        cv.namedWindow('Calibration', cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty('Calibration',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
        img1= cv.imread("D:/Git/ptut/src/view/images/charucoboard.jpg",0)
        cv.imshow('Calibration',img1)
        cv.waitKey(3000)
        _, img2 = cap.read()
        cv.destroyWindow('Calibration')


        #img2= cv.imread("D:/Git/ptut/src/view/images/test.jpg")
        
        
        cap.release()

        # Initiate SIFT detector
        sift = cv.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1,None)
        kp2, des2 = sift.detectAndCompute(img2,None)
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        flann = cv.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1,des2,k=2)
        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)
        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
            M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()
            h,w = img1.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv.perspectiveTransform(pts,M)
            print("dst:")
            print(dst)
            img2 = cv.polylines(img2,[np.int32(dst)],True,255,3, cv.LINE_AA)
            print(M)
        else:
            print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
            matchesMask = None
              
        
        print("fin homographie")
        return M

    
