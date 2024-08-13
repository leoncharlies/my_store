from find_blob import find_blobs, find_blobs_random, draw_on_image_rect, find_laser_point_position
from utils import initlize_camera
import cv2

class catcher:
    def __init__(self):
        self.cap = initlize_camera(0)
        self.corner_location=[]
        self.is_write_down=False

    def find_blob(self,stop_event):
        while not stop_event.is_set():
            ret,frame=self.cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            result = find_laser_point_position(frame)
            if self.is_write_down:
                self.corner_location.append(result)
                self.is_write_down=False
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            stop_event.wait(0.01)
        self.exit() 

    def exit(self):
        self.cap.release()
        cv2.destroyAllWindows()

t = catcher()