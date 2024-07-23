import cv2
import numpy as np
from utils import open_operation,initialize_camera,read_frame,sent_data
import math
import time

usual_run=bytearray([0xFE,0xBC,0x01,0xEF])
slight_right=bytearray([0xFE,0xBC,0x02,0xEF])
slight_left=bytearray([0xFE,0xBC,0x03,0xEF])
turn_left=bytearray([0xFE,0xBC,0x04,0xEF])
turn_right=bytearray([0xFE,0xBC,0x05,0xEF])
stop=bytearray([0xFE,0xBC,0x00,0xEF])
cross_run=bytearray([0xFE,0xBC,0x06,0xEF])
ROIS = {
    'top': (160, 30, 320, 120, 0.1),
    'mid': (160, 210, 320, 120, 0.3),
    'bot': (160, 360, 320, 120, 0.6),
    'left': (40, 30, 120, 420, 0.5),
    'right': (480, 30, 120, 420, 0.5)
}

lower=np.array([100, 43, 46])
upper=np.array([124, 255, 255])

class linefollower:
    def __init__(self,camera_id=0):
        self.camera = initialize_camera(camera_id)

    def find_blobs_in_rois(self,img,ROIS,lower,upper):
        result = {}
        for dir,(x,y,w,h,weight) in ROIS.items():
            roi=img[y:y+h,x:x+w]
            HSV=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
            mask= cv2.inRange(HSV,lower,upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            min_area = 100
            if contours:
                max_contour =max(contours,key=cv2.contourArea)
                if cv2.contourArea(max_contour) > min_area:
                    M = cv2.moments(max_contour)
                    cx = int(M['m10'] / M['m00']) if M['m00'] != 0 else -1
                    cy = int(M['m01'] / M['m00']) if M['m00'] != 0 else -1

                    x_rect, y_rect, w_rect, h_rect = cv2.boundingRect(max_contour)
                    rect = (x + x_rect, y + y_rect, w_rect, h_rect)
                    # 计算轮廓的外接矩形
                    result[dir]={
                        "cx":cx+x,
                        "cy":cy+y,
                        "rect":rect,
                        "weight":weight,
                        "blob_flag":True
                    }
                    cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)
                    cv2.drawMarker(img, (result[dir]['cx'], result[dir]['cy']), (255, 0, 0),
                                markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)
                else:
                    result[dir] = {
                        "cx": -1,
                        "cy": -1,
                        "rect": None,
                        "weight": weight,
                        "blob_flag": False
                    }
            else:
                result[dir] = {
                    "cx": -1,
                    "cy": -1,
                    "rect": None,
                    "weight": weight,
                    "blob_flag": False
                }
        return result
    def get_angle(self,img):
        blobs_in_rois=self.find_blobs_in_rois(img,ROIS,lower,upper)
        croid_sum = (blobs_in_rois['top']['cx'] * blobs_in_rois['top']['weight'] +
                 blobs_in_rois['mid']['cx'] * blobs_in_rois['mid']['weight'] +
                 blobs_in_rois['bot']['cx'] * blobs_in_rois['bot']['weight'])
        weight_sum = (blobs_in_rois['top']['weight'] +
                  blobs_in_rois['mid']['weight'] +
                  blobs_in_rois['bot']['weight'])
        if weight_sum != 0:
            cpos = croid_sum / weight_sum
            DAngle = -math.atan((cpos - 320) / 240)  # 假设中心点在图像中心 (320, 240)
            DAngle = math.degrees(DAngle)
        else:
            DAngle = 0  # 如果没有找到任何色块，可以设置一个默认值
    
        if abs(DAngle) > 10:
            if DAngle > 0:
                print("slight right")
                sent_data(slight_right)
                print("Turn Angle: %f" % DAngle)
            elif DAngle < 0:
                print("slight left")
                sent_data(slight_left)
                print("Turn Angle: %f" % DAngle)
        else:
            print("usual Run")
            sent_data(usual_run)
            print("Turn Angle: %f" % DAngle)
    
    def main(self):
        cap=self.camera
        while True:
            frame=read_frame(cap)
            img=open_operation(frame)
            self.get_angle(img=img)
            time.sleep(0.1)  # 控制循环的频率，这里设置为0.1秒一次
            cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
