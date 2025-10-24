# -*- coding: utf-8 -*-
"""
@File           : serial_config.py
@Description    : This is a config file, which defined the constant variables.
@Author         : CharlesYu
@Created        : 2025/7/15
@Last Modified  : 2025/7/15
"""
# ------------------------------      Import     ------------------------------

# ------------------------------ Variable define ------------------------------
BAUDRATE_TEXT_TO_VALUE = {
    "9600": 9600,
    "19200": 19200,
    "38400": 38400,
    "57600": 57600,
    "115200": 115200,
}
BAUDRATE_VALUE_TO_TEXT = {
    9600: "9600",
    19200: "19200",
    38400: "38400",
    57600: "57600",
    115200: "115200",
}

BYTESIZE_TEXT_TO_VALUE = {
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
}
BYTESIZE_VALUE_TO_TEXT = {
    5: '5',
    6: '6',
    7: '7',
    8: '8',
}

STOPBITS_TEXT_TO_VALUE = {
    '1': 1,
    '2': 2,
}
STOPBITS_VALUE_TO_TEXT = {
    1: '1',
    2: '2',
}

PARITY_TEXT_TO_VALUE = {
    "None": 'N',
    "Even": 'E',
    "Odd": 'O',
}
PARITY_VALUE_TO_TEXT = {
    'N': "None",
    'E': "Even",
    'O': "Odd",
}

DEFAULT_PORT_CONFIG = {
    "baudrate": 115200,
    "bytesize": 8,
    "parity": 'N',
    "stopbits": 1,
    "timeout": 0.05,
}
