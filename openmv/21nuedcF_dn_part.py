import sensor, image, time
import uos, machine
import pyb
import KPU as kpu

# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)

# 加载.kmodel文件
task = kpu.load("/sd/your_model.kmodel")  # 确保.kmodel文件路径正确
anchor = (0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828)
kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)  # 修改阈值和锚点

# 初始化串口
uart = pyb.UART(3, 115200)  # 使用UART3，波特率115200

while True:
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)

    if code:
        for i in code:
            img.draw_rectangle(i.rect())
            label = i.classid()
            score = i.value()
            # 输出到串口
            uart.write(f'Label: {label}, Score: {score:.2f}, Rect: {i.rect()}\n')

            # 在OpenMV IDE中显示结果
            print(f'Label: {label}, Score: {score:.2f}, Rect: {i.rect()}')

kpu.deinit(task)
