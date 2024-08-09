import cv2
import numpy as np
import math
from utils import read_frame,initialize_camera

ROIS = {
    'top': (160, 30, 320, 120, 0.1),
    'mid': (160, 210, 320, 120, 0.3),
    'bot': (160, 360, 320, 120, 0.6),
    'left': (40, 30, 120, 420, 0.5),
    'right': (480, 30, 120, 420, 0.5)
}
lower = np.array([0, 100, 100])
upper = np.array([10, 255, 255])

def find_rois_blob(img):
    blobs_in_rois = {}
    for roi_direction, roi in ROIS.items():
        x, y, w, h, weight = roi
        roi_img = img[y:y+h, x:x+w]
        hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        max_area = 100  # 设置最小面积阈值为 100 像素
        
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            contour_area = cv2.contourArea(max_contour)
            
            if contour_area > max_area:
                M = cv2.moments(max_contour)
                cx = int(M['m10'] / M['m00']) if M['m00'] != 0 else -1
                cy = int(M['m01'] / M['m00']) if M['m00'] != 0 else -1

                # 计算轮廓的外接矩形
                x_rect, y_rect, w_rect, h_rect = cv2.boundingRect(max_contour)
                rect = (x + x_rect, y + y_rect, w_rect, h_rect)

                blobs_in_rois[roi_direction] = {
                    'rect': rect,
                    'cx': x + x_rect + w_rect // 2,  # 矩形中心 x 坐标
                    'cy': y + y_rect + h_rect // 2,  # 矩形中心 y 坐标
                    'blob_flag': True,
                    'weight': weight
                }

                # 绘制矩形
                cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)

                # 绘制中心十字标记
                cv2.drawMarker(img, (blobs_in_rois[roi_direction]['cx'], blobs_in_rois[roi_direction]['cy']), (255, 0, 0),
                               markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)
            else:
                blobs_in_rois[roi_direction] = {
                    'rect': None,
                    'cx': -1,
                    'cy': -1,
                    'blob_flag': False,
                    'weight': weight
                }
        else:
            blobs_in_rois[roi_direction] = {
                'rect': None,
                'cx': -1,
                'cy': -1,
                'blob_flag': False,
                'weight': weight
            }
    return blobs_in_rois

def tracing(frame):
    # 循迹算法
    cap=initialize_camera(0)
    frame =read_frame(cap=cap)
    


