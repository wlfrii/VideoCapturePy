import cv2
import numpy as np

class Camera():
    '''A camera class used to initialize the camera, read image '''
    def __init__(self, idx, image_width, image_height, sharpness=3, backlight=0):
        self.idx = idx
        self.image_width = image_width
        self.image_height = image_height
        self.sharpness = sharpness
        self.backlight = backlight
        # default properties
        self.cap = cv2.VideoCapture(idx)

        tmp = np.zeros((image_height, image_width, 3), dtype="uint8")
        self.non_frame = cv2.putText((tmp), 'NO SIGNAL', (int(self.image_width/3.95), int(self.image_height/1.83)), cv2.FONT_HERSHEY_COMPLEX, 5, (255, 255, 255),5)

        self.initCapture()

    def initCapture(self):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.image_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.image_height)
        self.cap.set(cv2.CAP_PROP_SHARPNESS, self.sharpness)
        self.cap.set(cv2.CAP_PROP_BACKLIGHT, self.backlight)

    def getFrame(self):
        ret,frame = self.cap.read()
        if not ret:
            self.cap.release()
            self.cap.open(self.idx)
            self.initCapture()

            return self.non_frame
        else:
            return frame

    def release(self):
        self.cap.release()