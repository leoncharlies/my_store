#!/usr/bin/python
# coding:utf-8
# servo_PWM_GPIO_zero.py
# 树莓派GPIO控制外部舵机来回摆动，角度范围为0~180°，周期为4秒。

from gpiozero import PWMOutputDevice
import time

def servo_map(before_value, before_range_min, before_range_max, after_range_min, after_range_max):
    """
    功能:将某个范围的值映射为另一个范围的值
    参数：原范围某值，原范围最小值，原范围最大值，变换后范围最小值，变换后范围最大值
    返回：变换后范围对应某值
    """
    percent = (before_value - before_range_min) / (before_range_max - before_range_min)
    after_value = after_range_min + percent * (after_range_max - after_range_min)
    return after_value

# 定义GPIO引脚
servo_SIG1 = 14
servo_SIG2 = 15
servo_freq = 50
servo_time = 0.01
servo_width_min = 2.5
servo_width_max = 12.5

# 创建PWMOutputDevice对象
servo1 = PWMOutputDevice(pin=servo_SIG1, frequency=servo_freq, initial_value=0)
servo2 = PWMOutputDevice(pin=servo_SIG2, frequency=servo_freq, initial_value=0)
print('预设置完成，两秒后开始摆动')
time.sleep(2)

try:
    while True:
        for dc in range(1, 181, 1):
            dc_trans = servo_map(dc, 0, 180, servo_width_min, servo_width_max) / 100.0
            servo1.value = dc_trans
            servo2.value = dc_trans
            time.sleep(servo_time)
        time.sleep(0.2)
        for dc in range(180, -1, -1):
            dc_trans = servo_map(dc, 0, 180, servo_width_min, servo_width_max) / 100.0
            servo1.value = dc_trans
            servo2.value = dc_trans
            time.sleep(servo_time)
        time.sleep(0.2)
except KeyboardInterrupt:
    pass

servo1.value = 0  # 停止PWM输出
servo2.value = 0  # 停止PWM输出