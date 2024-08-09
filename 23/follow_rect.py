import cv2
import numpy as np

color_threashold = {
    'lower': np.array([0, 0, 0]),
    'upper': np.array([180, 255, 46])
}
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

def draw_on_image(image,result):
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
            
