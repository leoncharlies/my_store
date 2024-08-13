from gpiozero import PWMOutputDevice
import time
import math
servo_SIG1 = 14
servo_SIG2 = 15
servo_freq = 100
servo_time = 0.01
servo_width_min = 0
servo_width_max = 1
class motor_controller:
    def __init__(self):
        # 初始化
        # 横向电机
        self.servo1 = PWMOutputDevice(pin=servo_SIG1, frequency=servo_freq, initial_value=0.5)    
        # 纵向电机
        self.servo2 = PWMOutputDevice(pin=servo_SIG2, frequency=servo_freq, initial_value=0.5)
        self.x_width = 0
        self.y_width = 0
    def servo_map(before_value, before_range_min, before_range_max, after_range_min, after_range_max):
        """
        功能:将某个范围的值映射为另一个范围的值
        参数：原范围某值，原范围最小值，原范围最大值，变换后范围最小值，变换后范围最大值
        返回：变换后范围对应某值
        """
        percent = (before_value - before_range_min) / (before_range_max - before_range_min)
        after_value = after_range_min + percent * (after_range_max - after_range_min)
        return after_value
    def steering_reset(self):   #将舵机复位
        self.servo1.value = 0.5
        self.servo2.value = 0.5
    def set_width(self,x,y):
        self.x_width = x
        self.y_width = y

    def coor2angle(self,cx,cy):
        """
        功能:将坐标系中的坐标转换为舵机角度
        参数：x,y坐标
        返回：舵机角度
        """
        x_angle=math.atan(cx*0.5/self.x_width)
        y_angle=math.atan(cy*0.5/self.y_width)
        return [x_angle,y_angle]

    def folllow_pencil_line(self,coor_list):
        pass