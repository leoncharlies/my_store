from find_blob import find_blobs,find_blobs_random,draw_on_image_rect,find_laser_point_position
from utils import read_frame,initlize_camera
import cv2
class test:
    def __init__(self):
        self.cap=initlize_camera(0)

    
    def main(self):
        while True:
            self.image=read_frame(self.cap)
            result=find_laser_point_position(self.image)
            cv2.imshow('frame',self.image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

t=test()
t.main()

