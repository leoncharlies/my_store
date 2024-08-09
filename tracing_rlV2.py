import cv2
import numpy as np
import math

# 初始化摄像头
cap = cv2.VideoCapture(0)  # 通常摄像头编号为 0，如果有多个摄像头可能需要调整编号

# 设置摄像头分辨率为 640x480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ROI 定义
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

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    blobs_in_rois = find_rois_blob(frame)
    
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
    
    if abs(DAngle) > 20:
        if DAngle > 0:
            print("Turn right")
            print("Turn Angle: %f" % DAngle)
        elif DAngle < 0:
            print("Turn left")
            print("Turn Angle: %f" % DAngle)
    else:
        print("Run")
        print("Turn Angle: %f" % DAngle)
    
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

