import cv2
import numpy as np

# 加载ONNX模型
net = cv2.dnn.readNetFromONNX('yolov5s.onnx')

# 打开摄像头
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 图像预处理
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1/255.0, size=(640, 640), swapRB=True, crop=False)
    net.setInput(blob)

    # 前向传播，获得检测结果
    detections = net.forward()

    # YOLOv5的输出是一个N x 85的张量，其中N是检测到的目标数量，85表示每个目标的85个属性
    # 属性包括：4个边界框坐标，1个置信度分数和80个类别概率
    rows = detections.shape[0]

    for i in range(rows):
        # 获取每个检测的置信度分数
        confidence = detections[i, 4]
        
        # 置信度阈值
        if np.any(confidence > 0.5):
            # 获取边界框坐标
            x_center = int(detections[i, 0] * frame.shape[1])
            y_center = int(detections[i, 1] * frame.shape[0])
            width = int(detections[i, 2] * frame.shape[1])
            height = int(detections[i, 3] * frame.shape[0])

            # 计算边界框的左上角坐标
            x1 = int(x_center - width / 2)
            y1 = int(y_center - height / 2)
            x2 = int(x_center + width / 2)
            y2 = int(y_center + height / 2)

            # 绘制边界框和置信度
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f'Confidence: {confidence:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 显示结果图像
    cv2.imshow('YOLOv5 Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
