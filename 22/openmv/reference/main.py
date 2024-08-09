import sensor, image, time, math,pyb
from pyb import UART
led = pyb.LED(1)                      ##提示灯
GRAYSCALE_THRESHOLD = [(0, 64)]       ##选择灰度阈值，可根据不同情况进行调整
ROIS = [
        (0, 0, 160, 30, 0.7),
        (0, 30, 160, 60, 0.3),
        (0, 90, 160, 30, 0.1)
       ]                              ##选择ROI感兴趣区，将视野进行分割
weight_sum = 0
for r in ROIS: weight_sum += r[4]
sensor.reset()                        ##初始化
sensor.set_pixformat(sensor.GRAYSCALE)##选择灰度模式
sensor.set_framesize(sensor.QQVGA)    ##选择分辨率（分辨率越高帧率可能越低）
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)           ##关闭自动增益
sensor.set_auto_whitebal(False)       ##关闭白平衡
clock = time.clock()
uart = UART(3, 115200)                ##确定串口波特率
uart.init(115200, bits=8, parity=None, stop=1) ##串口初始化
in_flag = 1                            ##内圈flag
out_flag = 0                           ##外圈flag
def out_turn():
 for r in ROIS:
    blobs = img.find_blobs(GRAYSCALE_THRESHOLD, merge=True)   ##寻找符合阈值的色块
    if blobs:
           largest_blob = max(blobs, key=lambda b: b.pixels()) ##寻找所有符合要求的色块中面积最大的一个
           Area=largest_blob.area()                            ##获得面积，方便判断之后停车线的面积阈值
           img.draw_rectangle(largest_blob.rect())
           img.draw_cross(largest_blob.cx(),
                           largest_blob.cy())
           data = bytearray([0xAA, largest_blob.cy(), 0, 0XBB])  ##与单片机通信部分
           uart.write(data)
           print(Area,largest_blob.cy())
           if((largest_blob.cy() >= 50 and largest_blob.cy() <= 70) and Area >= 12000):  ##判断停车线（两重判断）
            data = bytearray([0xAA, largest_blob.cy(), 1, 0XBB]) ##与单片机通信部分
            uart.write(data)
            print(largest_blob.cy())
            print(666)
            led.on()                                           ##判断到停车线时提示灯亮起
def in_turn():
  for r in ROIS:
        blobs = img.find_blobs(GRAYSCALE_THRESHOLD,merge=True)  ##寻找符合阈值的色块
        if blobs:
             largest_blob = max(blobs, key=lambda b: b.pixels())  ##寻找所有符合要求的色块中面积最大的一个
             Area=largest_blob.area()                             ##获得面积，方便判断之后停车线的面积阈值
             print(Area)
             img.draw_rectangle(largest_blob.rect())
             img.draw_cross(largest_blob.cx(),
                            largest_blob.cy())
             if(Area>=8000 and largest_blob.cy()<=50):            ##内外圈岔道口判断
              blobs2 = img.find_blobs(GRAYSCALE_THRESHOLD,roi=(53,0,107,65),merge=True)
              if blobs2:
               largest_blob = max(blobs2, key=lambda b: b.pixels())
               data = bytearray([0xAA, largest_blob.cy(),0,0XBB])
               uart.write(data)
              # print(789)                                       ##从终端上确认数据已发送
             else:
              data = bytearray([0xAA, largest_blob.cy(),0,0XBB])
              uart.write(data)
             print(largest_blob.cy())
             if((largest_blob.cy() >= 55 and largest_blob.cy() <= 65) and Area >= 12000): ##判断停车线（两重判断）
              data = bytearray([0xAA, largest_blob.cy(), 1, 0XBB])
              uart.write(data)
              print(largest_blob.cy())
             # print(666)                                        ##从终端上确认数据已发送
while(True):
   clock.tick()
   img = sensor.snapshot()
   if uart.any():   ##收到单片机发送来的数据 （0是外圈，1是内圈）
    a=uart.readline()
    print(a[0])
    if(a[0]==0):
     (out_flag == 1)
    # print("in_flag")
     in_turn()
    if(a[0] == 1):
     (in_flag == 1)
     out_turn()
   #print(clock.fps())  ##测试帧率
