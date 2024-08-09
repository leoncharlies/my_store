import torch
import cv2

# 确保已在本地克隆 YOLOv5 仓库
# git clone https://github.com/ultralytics/yolov5
# cd yolov5

# 导入 yolov5
import sys
sys.path.append('./yolov5')  # 修改为 YOLOv5 仓库的实际路径
from models.common import DetectMultiBackend

# 加载本地训练好的模型
model = DetectMultiBackend('yolov5/runs/train/exp4/weights/best.pt')

def detect(image):
    # 将图像转换为适合模型的格式
    results = model(image)
    return results

def main():
    cap = cv2.VideoCapture(0)  # 选择摄像头
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # YOLOv5 检测
        results = detect(frame)

        # 处理检测结果
        for det in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = det
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f'{results.names[int(cls)]} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('YOLOv5 Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
