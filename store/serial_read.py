import serial

# 打开串口
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

try:
    while True:
        # 读取一个字节的数据
        byte = ser.read(1)
        if byte:
            # 解码字节数据
            char = byte.decode('utf-8')
            
            if char == 'N':
                # 读取接下来的三个字符
                remaining_data = ser.read(3)
                if remaining_data:
                    decoded_data = (char + remaining_data.decode('utf-8')).strip()
                    print("Received data starting with 'N':", decoded_data)
                    # 这里可以添加更多处理逻辑

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # 关闭串口
    ser.close()
