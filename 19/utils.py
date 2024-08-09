import cv2
import numpy as np
import time
import serial

def initialize_camera():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return cap

def get_frame(cap):
    ret, frame = cap.read()
    return frame

class com:
    def __init__(self):
        self.ser=serial.Serial('com_name',115200) # Establish the connection on a specific port
        self.received_data=None
    #    self.thread = threading.Thread(target=self.read_data)
    #    self.thread.daemon = True
    #    self.thread.start()
    def send_data(self,data):
        self.ser.write(data)

    def receive_data(self):
        self.received_data=self.ser.readline().decode('utf-8').rstrip('\n')
    
    def deliver_data(self):
        return self.received_data