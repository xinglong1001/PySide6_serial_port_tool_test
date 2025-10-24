# -*- coding: utf-8 -*-
"""
@File           : modbus_parse.py
@Description    : This is a command file, which is used to control the hotplate slave device.
Including commands, switch method, read method, write method and so on.
@Author         : CharlesYu
@Created        : 2025/07/08
@Last Modified  : 2025/07/16
"""

# ------------------------------ Import ------------------------------
from enum import Enum

# ------------------------------ Variable define ------------------------------
class AppVars:
    def __init__(self):
        self.port_list = []
        self.port_list_name = []
        self.port_list_info = []
        self.port = None
        self.baudrate = None
        self.bytesize = None
        self.stopbits = None
        self.parity = None

app_vars = AppVars()
