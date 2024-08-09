from tracing_rl import linefollower
import cv2
import numpy as np
import time
from utils import open_operation,initialize_camera,read_frame,com

usual_run=bytearray([0xFE,0xBC,0x01,0xEF])
slight_right=bytearray([0xFE,0xBC,0x02,0xEF])
slight_left=bytearray([0xFE,0xBC,0x03,0xEF])
turn_left=bytearray([0xFE,0xBC,0x04,0xEF])
turn_right=bytearray([0xFE,0xBC,0x05,0xEF])
stop=bytearray([0xFE,0xBC,0x00,0xEF])
cross_run=bytearray([0xFE,0xBC,0x06,0xEF])

class car:
    def __init__(self):
         self.count=0
    def motion(self,DAngle,mode):
        if abs(DAngle) > 10:
            if DAngle > 0:
                    print("slight right")
                    com.sent_data(slight_right)
                    print("Turn Angle: %f" % DAngle)
            elif DAngle < 0:
                    print("slight left")
                    com.sent_data(slight_left)
                    print("Turn Angle: %f" % DAngle)
        else:
                print("usual Run")
                com.sent_data(usual_run)
                print("Turn Angle: %f" % DAngle)


    def main(self):
        lf=linefollower(0)
        cap=lf.camera
        while True:
            frame=read_frame(cap)
            img=open_operation(frame)
            lf.get_angle(img=img)
            self.motion(lf.DAngle,lf.mode)
            time.sleep(0.1)  # 控制循环的频率，这里设置为0.1秒一次
            cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cap.release()
            cv2.destroyAllWindows()

Raspicar=car()
Raspicar.main()
