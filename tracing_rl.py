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
    'top': (160,30, 320, 120, 0.1),
    'mid': (160, 180, 320, 120, 0.3),
    'bot': (160, 330, 320, 120, 0.6),
    'left': (40, 160, 30, 450, 0.5),
    'right': (480,600,30, 450, 0.5)
}
lower = np.array([0, 43, 46])
upper = np.array([10, 255, 255])

def find_rois_blob(img):
    blobs_in_rois = {}
    for roi_direction, roi in ROIS.items():
        x, y, w, h, weight = roi
        roi_img = img[y:h, x:w]
        hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(max_contour)
            cx = int(M['m10'] / M['m00']) if M['m00'] != 0 else -1
            cy = int(M['m01'] / M['m00']) if M['m00'] != 0 else -1
            blobs_in_rois[roi_direction] = {
                'cx': cx,
                'cy': cy,
                'blob_flag': True,
                'weight': weight
            }
            cv2.drawContours(img, [max_contour], -1, (255, 0, 0), 2)  # 绘制轮廓
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)  # 绘制质心
        else:
            blobs_in_rois[roi_direction] = {
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
        DAngle = -math.atan((cpos - 40) / 30)
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
