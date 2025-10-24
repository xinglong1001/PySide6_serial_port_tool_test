# -*- coding: utf-8 -*-
"""
@File           : utils.py
@Description    : This is used for developing general function.
@Author         : CharlesYu
@Created        : 2025/08/10
@Last Modified  : 2025/08/10
"""
# ------------------------------ Import ------------------------------

# ------------------------------ Variable define ------------------------------

# ------------------------------ Function define ------------------------------
def hex_to_str(bs: bytes) -> str:
    return ' '.join(f'0x{b:02x}' for b in bs)