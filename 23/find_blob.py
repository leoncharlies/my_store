import cv2
import numpy as np

color_threashold = {
    'lower': np.array([0, 100, 100]),  # 或者[0, 50, 50]根据具体情况调整
    'upper': np.array([10, 255, 255])
}

lower_red1 = np.array([0, 50, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 50, 50])
upper_red2 = np.array([180, 255, 255])

lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 55, 255])

min_area=100
def find_blobs(image):                                  #仅适用于正放的方框
    result={'x':-1,'y':-1,'w':-1,'h':-1,'flag':False}
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,color_threashold['lower'],color_threashold['upper'])
    contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_contour=max(contours,key=cv2.contourArea)
        if cv2.contourArea(max_contour)>min_area:
            x,y,w,h=cv2.boundingRect(max_contour)
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            result={'x':x,'y':y,'w':w,'h':h,'flag':True}
        else:
            print("No object found")
    return result

def draw_on_image_rect(image,result):
    if result['flag']:
        cv2.rectangle(image,(result['x'],result['y']),(result['x']+result['w'],result['y']+result['h']),(0,255,0),2)
        print("x:{}, y:{}, w:{}, h:{}".format(result['x'],result['y'],result['w'],result['h']))
    return image

def find_blobs_random(image):                           #适用于斜放的方框
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 应用阈值
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    # 找到轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 画出轮廓
    for contour in contours:
        # 过滤掉非矩形的轮廓
        epsilon = 0.02 * cv2.arcLength(contour, True)           #根据轮廓的边长确定下面的参数值
        approx = cv2.approxPolyDP(contour, epsilon, True)       #使用Douglas–Peucker算法来求出
        
        if len(approx) == 4:
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
            points = approx.reshape(4, 2)                       # 提取四个顶点坐标
            for point in points:
                print(point) 
            result=[points,True]


def find_laser_point_position(image):
    result = {'x': -1, 'y': -1, 'flag': False}
    
    # 转换为 HSV 色彩空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 获取白色的掩膜
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    contours, _ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # 查找面积最大的轮廓
        max_contour = max(contours, key=cv2.contourArea)
        
        # 如果轮廓的面积超过一定阈值（排除噪声）
        if cv2.contourArea(max_contour) > 10:  # 面积阈值可以根据实际情况调整
            M = cv2.moments(max_contour)
            if M['m00'] != 0:
                # 计算中心坐标
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                result = {'x': cx, 'y': cy, 'flag': True}
    
    # 可视化结果
    if result['flag']:
        cv2.circle(image, (result['x'], result['y']), 5, (0, 255, 0), -1)
        print("x:{}, y:{}".format(result['x'], result['y']))
    else:
        #print("Laser point not found")
        pass
    
    return result