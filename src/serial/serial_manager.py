# -*- coding: utf-8 -*-
"""
@File           : serial_manager.py
@Description    : This is a serial port config file, which is used to do some operations
related to serial port.
@Author         : CharlesYu
@Created        : 2025/7/08
@Last Modified  : 2025/7/16
"""
# ------------------------------      Import     ------------------------------
import time
import serial.tools.list_ports

from src.serial.serial_config import DEFAULT_PORT_CONFIG


# ------------------------------ Function define ------------------------------
class SerialManager:
    def __init__(self):
        self.port_list = None
        self.port_list_name = []
        self.ser = serial.Serial()
        self.write_resp_size = 8
        self.ser.baudrate = DEFAULT_PORT_CONFIG["baudrate"]
        self.ser.bytesize = DEFAULT_PORT_CONFIG["bytesize"]
        self.ser.stopbits = DEFAULT_PORT_CONFIG["stopbits"]
        self.ser.parity = DEFAULT_PORT_CONFIG["parity"]
        self.ser.timeout = DEFAULT_PORT_CONFIG["timeout"]

        self.recv_bytes_counts = 0      #lyx for statics recive bytes && send bytes
        self.send_bytes_counts = 0

    # ---------- Basic method
    @staticmethod
    def get_port_info():
        """
        This is a serial manager func, which is used to get all
        the serial ports and return the information list
        and name list.
        :param: None
        :return : port_list, port_list_name
        """
        port_list = serial.tools.list_ports.comports()
        port_list_name = []
        port_list_info = []
        for port in port_list:
            port_list_name.append(port.device)
            port_list_name.reverse()
            port_list_info.append(port.device + ' - ' + port.description)
            port_list_info.reverse()
            # print(f"串口 - {port.device}")
        # print(f"port list: {port_list}")
        # print(f"port list name: {port_list_name}")
        # print(f"port list info: {port_list_info}")
        return port_list, port_list_name, port_list_info

    def configure(self, port, baud, bytesize, stopbits, parity):
        """
        This is a serial manger func, which is used to configure the serial port.
        :param port: Port name.
        :param baud: Baudrate
        :param bytesize: Bytesize
        :param stopbits: Stopbits
        :param parity: Parity
        :return:
        """
        self.ser.port = port
        self.ser.baudrate = baud
        self.ser.bytesize = bytesize
        self.ser.stopbits = stopbits
        self.ser.parity = parity
        # print(
        #     f"Configure serial port: {self.ser.port} {self.ser.baudrate} {self.ser.bytesize} {self.ser.stopbits} {self.ser.parity}")

    def open(self) -> bool:
        """
        This is a serial manager func, which is used to open the serial port.
        :return:
        """
        if self.ser.is_open:
            return True
        try:
            self.ser.open()
            print(f"Serial port {self.ser.name} is opened successfully.")
            return True
        except serial.SerialException as e:
            print(f"Failed to open serial port {self.ser.name}: {e}")
            return False

    def is_open(self):
        return self.ser.is_open

    def close(self):
        """
        This is a serial manager func, which is used to close the serial port.
        :return:
        """
        if self.ser.is_open:
            self.ser.close()
            print(f"Serial port {self.ser.name} is closed successfully.")

    def write_ascii(self, data):
        """
        This is a serial manager func, which is used to send one frame data
        to serial port.
        :param data:
        :return:
        """
        if self.ser and self.ser.is_open:
            self.ser.write(data.encode())
            self.send_bytes_counts+= len(data)      # lyx send byte statics 

    def read_bytes(self, size: int) -> bytes:
        """Read exactly `size` bytes from the serial port, with timeout."""
        data = self.ser.read(size)
        if len(data) != size:
            return None
        return data

    def read_bytes_with_timeout(self, size: int, timeout=1.0) -> bytes:
        data = b""
        start_time = time.time()
        while len(data) < size:
            if self.ser.in_waiting > 0:
                need = size - len(data)
                data += self.ser.read(min(self.ser.in_waiting, need))
            if time.time() - start_time > timeout:
                return b""
            time.sleep(0.01)
        return data

    def read_line(self, timeout=1.0):
        """
        This is a serial manager func, which is used to receive data from
        serial port.
        :return:
        """
        start_time = time.time()
        while start_time - time.time() < timeout:
            if self.ser.in_waiting > 0:
                return self.ser.readline()
            time.sleep(0.05)
        return None

    # ---------- Modbus business
    def send_modbus_request(self, bytes):
        if self.ser and self.ser.is_open:
            self.ser.write(bytes)

    def read_modbus_reading_response(self, timeout=1.0) -> bytes:
        header = self.read_bytes_with_timeout(3, timeout)
        if not header:
            return b""
        slave_addr, func, byte_count = header
        data = self.read_bytes_with_timeout(byte_count, timeout)
        if not data:
            return b""
        crc = self.read_bytes_with_timeout(2, timeout)
        if not data:
            return b""
        return header + data + crc

    def read_modbus_write_response(self, timeout=1.0) -> bytes:
        resp = b""
        start_time = time.time()
        while len(resp) < self.write_resp_size:
            if self.ser.in_waiting > 0:
                need = self.write_resp_size - len(resp)
                resp += self.ser.read(min(self.ser.in_waiting, need))
            if time.time() - start_time > timeout:
                break
            time.sleep(0.01)
        return resp
