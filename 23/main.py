import cv2
import numpy as np
from utils import initlize_camera,read_frame
from follow_rect import find_blobs,draw_on_image

class catcher:
    def __init__(self):
        self.cap=initlize_camera(0)
    
    def main(self):
        while True:
            frame=read_frame(self.cap)
            blob=find_blobs(frame)
            img=draw_on_image(frame,blob)
            cv2.imshow('frame',img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()


c=catcher()
c.main()
