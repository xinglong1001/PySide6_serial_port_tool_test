#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import sys

# ==========================
# 配置串口
# ==========================
SERIAL_PORT = '/dev/ttyS0'  # 修改为你的串口设备
BAUD_RATE = 9600
TIMEOUT = 1

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
    print("串口已打开: {}".format(SERIAL_PORT))
except Exception as e:
    print("无法打开串口: {}".format(e))
    sys.exit(1)

print("输入 'exit' 退出程序")

# ==========================
# 交互循环
# ==========================
while True:
    # 输入要发送的数据
    user_input = raw_input("发送: ")  # Python 2
    if user_input.lower() == 'exit':
        break

    # 发送数据
    ser.write(user_input.encode() + b'\n')

    # 等待设备返回数据
    time.sleep(0.2)
    while ser.inWaiting() > 0:
        recv_data = ser.readline()
        print("接收: {}".format(recv_data.strip()))

# ==========================
# 关闭串口
# ==========================
ser.close()
print("串口已关闭")
