#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import threading
import sys

def read_from_port(ser):
    """后台线程，实时接收串口数据"""
    while True:
        try:
            data = ser.read(ser.in_waiting or 1)
            if data:
                print("\n[Received]:", data.decode(errors='replace'))
                print("> ", end="", flush=True)
        except Exception as e:
            print(f"\n[Error receiving]: {e}")
            break

def main():
    # 配置串口
    port = input("Enter serial port (e.g., /dev/ttyS0): ").strip()
    baudrate = input("Enter baudrate (default 9600): ").strip()
    baudrate = int(baudrate) if baudrate else 9600

    try:
        ser = serial.Serial(port, baudrate, timeout=0.1)
    except Exception as e:
        print(f"Failed to open serial port {port}: {e}")
        sys.exit(1)

    print(f"Opened {port} at {baudrate} bps. Type your message and press Enter to send.")
    print("Press Ctrl+C to exit.\n")

    # 启动接收线程
    t = threading.Thread(target=read_from_port, args=(ser,), daemon=True)
    t.start()

    # 主线程用于发送
    try:
        while True:
            msg = input("> ")
            if msg:
                ser.write(msg.encode())
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
