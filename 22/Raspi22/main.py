from tracing_rl import linefollower
import cv2
import numpy as np
import time
from utils import open_operation,initialize_camera,read_frame,com

usual_run=bytearray([0xFE,0xBC,0x01,0xEF])
slight_right=bytearray([0xFE,0xBC,0x02,0xEF])
slight_slight_right=bytearray([0xFE,0xBC,0x07,0xEF])
slight_left=bytearray([0xFE,0xBC,0x03,0xEF])
slight_slight_left=bytearray([0xFE,0xBC,0x08,0xEF])
turn_left=bytearray([0xFE,0xBC,0x04,0xEF])
turn_right=bytearray([0xFE,0xBC,0x05,0xEF])
stop=bytearray([0xFE,0xBC,0x00,0xEF])
cross_run=bytearray([0xFE,0xBC,0x06,0xEF])

class car:
    def __init__(self):
         self.count=0
         self.com=com()
         self.flag_start=0          #初始启动判断的程序

    def flag_check(self):
        data = self.com.get_data().strip()  # 去除前后空白字符
        # print(f"Checking flag, received_data: '{data}' (type: {type(data)})")  # 调试用打印
        # print(f"Received data length: {len(data)}")  # 打印数据长度
        # print(f"Received data repr: {repr(data)}")  # 打印数据的repr，显示隐藏字符

        if data == 'N':
            self.flag_start = 0
        if data == 'Y':
            self.flag_start = 1

        
    def motion(self,DAngle,flag,mode,traceback):
        if traceback==0:
            print("stop")
            self.com.sent_data(stop)
        else:
            if flag==1:
                print("cross_run")
                self.com.sent_data(cross_run)
            else:
                if abs(DAngle) > 4:
                    if abs(DAngle) <30:
                        if DAngle < 0:
                            print("slight slight right")
                            self.com.sent_data(slight_slight_right)
                            print("Turn Angle: %f" % DAngle)
                        elif DAngle > 0:
                            print("slight slight left")
                            self.com.sent_data(slight_slight_left)
                            print("Turn Angle: %f" % DAngle)
                    else:
                        if DAngle < 0:
                                print("slight right")
                                self.com.sent_data(slight_right)
                                print("Turn Angle: %f" % DAngle)
                        elif DAngle > 0:
                                print("slight left")
                                self.com.sent_data(slight_left)
                                print("Turn Angle: %f" % DAngle)
                else:
                        print("usual Run")
                        self.com.sent_data(usual_run)
                        print("Turn Angle: %f" % DAngle)
    
    
    def main(self):
        lf=linefollower(0)
        cap=lf.camera
        print(self.com.received_data)
        while True:
            frame=read_frame(cap)
 #           img=open_operation(frame)
            lf.get_angle(img=frame)
            self.flag_check()
            self.motion(lf.angle,lf.model,lf.corner,self.flag_start)
            time.sleep(0.01)  # 控制循环的频率，这里设置为0.1秒一次
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            #print("flag_start: %d" % self.flag_start)
            #print("received_data: %s" % self.com.received_data)
        cap.release()
        cv2.destroyAllWindows()

Raspicar=car()
Raspicar.main()
