from src.Singleton import Singleton


class Camera(Singleton):
    def __init__(self):
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def __del__(self):
        self.cap.release()

    def read(self):
        return self.cap.read()


