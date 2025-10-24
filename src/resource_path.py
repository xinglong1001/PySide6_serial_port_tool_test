# -*- coding: utf-8 -*-
"""
@File           : resource_path.py
@Description    : 
@Author         : CharlesYu
@Created        : 2025/7/21
@Last Modified  : 2025/7/21
"""
# ------------------------------      Import     ------------------------------
import os
import sys


# ------------------------------ Variable define ------------------------------

# ------------------------------ Function define ------------------------------
def get_resource_path(relative_path: str) -> str:
    """
    获取资源文件的绝对路径。打包前为项目目录，打包后为临时目录。
    """
    if hasattr(sys, '_MEIPASS'):  # PyInstaller 打包后的临时目录
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath("./")
    return os.path.join(base_path, relative_path)
