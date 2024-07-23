import cv2
import numpy as np
import serial


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

def sent_data(mes):
    dev=serial.Serial('dev/ttyUSB0',115200)
    dev.write(mes)