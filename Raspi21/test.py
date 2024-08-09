import cv2
from utils import open_operation
img =cv2.imread('001.jpg',cv2.IMREAD_COLOR)
if img is None:
    print("Error: Unable to load image!")
else:
    # 调用open_operation函数
    processed_img = open_operation(img)
    scale_percent = 20  # 将图片缩放为原来的50%
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    resized_processed_img = cv2.resize(processed_img, dim, interpolation=cv2.INTER_AREA)

    cv2.imshow('Original Image', resized_img)
    cv2.imshow('Processed Image', resized_processed_img)
    # cv2.imwrite('processed.jpg', processed_img)
    # 等待用户按任意键关闭窗口
    cv2.waitKey(0)
    cv2.destroyAllWindows()