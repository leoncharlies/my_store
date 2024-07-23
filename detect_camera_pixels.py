import cv2

# 打开摄像头（0表示默认摄像头）
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("无法打开摄像头")
else:
    # 获取摄像头的宽度
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # 获取摄像头的高度
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    print(f"摄像头分辨率: {int(width)} x {int(height)}")

    # 释放摄像头
    cap.release()
    cv2.destroyAllWindows()
