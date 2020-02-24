from ams.loggable import Loggable
from matplotlib import pyplot as plt
import cv2

class Camera(Loggable):

    def __init__(self, identifier=0):
        self._cap = cv2.VideoCapture(identifier)
        self._cap.set(cv2.CAP_PROP_BUFFERSIZE, 1);
    def getframe(self):
        return self._cap.read()
    
    def capture(self, path):
        ret, frame = self.getframe()
        
        if ret:
            cv2.imwrite(path, frame)
        
        return ret         
  
