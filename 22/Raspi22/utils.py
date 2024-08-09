import cv2
import numpy as np
import serial
import threading

def initialize_camera(camera_index=0):
    """初始化打开摄像头，并设置分辨率"""
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    if not cap.isOpened():
        raise ValueError("Camera could not be opened.")
    return cap

def read_frame(cap):
    """读取帧"""
    ret, frame = cap.read()
    if not ret:
        raise ValueError("Failed to read frame from camera.")
    return frame

def open_operation(img):
    k=np.ones((7,7),np.uint8)
    img=cv2.erode(img,k)
    img=cv2.dilate(img,k)
    return img

class com:
    def __init__(self):
        self.dev=serial.Serial('/dev/ttyUSB0',115200)
        self.received_data ='X'
        self.thread = threading.Thread(target=self.read_data)
        self.thread.daemon = True
        self.thread.start()

    def sent_data(self,mes):
        self.dev.write(mes)

    def read_data(self):
        while True:
            if self.dev.in_waiting > 0:
                self.received_data = self.dev.read(self.dev.in_waiting).decode('utf-8')

    def get_data(self):
        return ''.join(filter(str.isprintable, self.received_data))                     # 去除所有非打印字符
