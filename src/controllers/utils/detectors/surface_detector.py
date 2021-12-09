#TODO: detecter la surface de jeu
import cv2
import numpy as np

class Surface:



    def __findCornerPoints__(self,transform):
        
        cv2.namedWindow('Calibration', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Calibration',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        img= cv2.imread("D:/Git/ptut/src/view/images/charucoboard.jpg")
        cv2.imshow('Calibration',img)
        cv2.waitKey(3000)
        cv2.destroyWindow('Calibration')
        cap = cv2.VideoCapture(0)
        #_, frame = cap.read()
        frame= cv2.imread("D:/Git/ptut/src/view/images/test.jpg")
        cap.release()
        sift = cv2.xfeatures2d.SIFT_create()
        kp_image, desc_image = sift.detectAndCompute(img, None)
        # Feature matching
        index_params = dict(algorithm=0, trees=5)
        search_params = dict()
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # trainimage
        kp_grayframe, desc_grayframe = sift.detectAndCompute(grayframe, None)
        matches = flann.knnMatch(desc_image, desc_grayframe, k=2)
        good_points = []
        for m, n in matches:
            if m.distance < 0.6 * n.distance:
                good_points.append(m)
        query_pts = np.float32([kp_image[m.queryIdx].pt for m in good_points]).reshape(-1, 1, 2)
        train_pts = np.float32([kp_grayframe[m.trainIdx].pt for m in good_points]).reshape(-1, 1, 2)
        matrix, mask = cv2.findHomography(query_pts, train_pts, cv2.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()

        h, w,_ = img.shape
        pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, matrix)
        print(dst[0])
        return dst

