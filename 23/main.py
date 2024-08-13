import cv2
import numpy as np
from utils import initlize_camera,read_frame
from find_blob import find_blobs_random,draw_on_image_rect
from catcher import catcher
from motor import motor_controller
from GUI import GUI_manager

if __name__ == "__main__":
    my_GUI=GUI_manager()
    my_GUI.mainloop()


