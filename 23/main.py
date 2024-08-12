import cv2
import numpy as np
from utils import initlize_camera,read_frame
from find_blob import find_blobs_random,draw_on_image_rect

class catcher:
    def __init__(self):
        self.cap=initlize_camera(0)
    
    def main(self):
        while True:
            frame=read_frame(self.cap)
            blob=find_blobs_random(frame)
            img=draw_on_image_rect(frame,blob)
            cv2.imshow('frame',img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()
    


c=catcher()
c.main()
