# -*- coding: utf-8 -*-
"""
@File           : serial_thread.py
@Description    : This is a QThread file, which is used to receive message from serial port in real time.
@Author         : CharlesYu
@Created        : 2025/07/16
@Last Modified  : 2025/07/16
"""
# ------------------------------      Import     ------------------------------
from PySide6.QtCore import QThread, Signal


# ------------------------------ Variable define ------------------------------
class SerialThread(QThread):
    data_received = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, ser):
        super().__init__()
        self.ser = ser
        self._running = True

    def run(self):
        """
        Rewrite the run func, receive the message from serial port
        :return: Received message
        """
        while self._running and self.ser.is_open:
            if self.ser.in_waiting > 0:
                try:
                    text = self.ser.readline().decode(errors="ignore")
                    self.data_received.emit(text)
                except Exception as e:
                    self.error_occurred.emit(f"[线程串口异常] {e}")

    def stop(self):
        """
        Stop this thread, when the serial port is closed or pushbutton
        is pressed and released during the port is opened.
        :return:
        """
        self._running = False
