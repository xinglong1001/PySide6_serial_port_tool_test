# -*- coding: utf-8 -*-
"""
@File           : main.py
@Description    : 
@Author         : CharlesYu
@Created        : 2025/8/25
@Last Modified  : 2025/8/25
"""
# ------------------------------      Import     ------------------------------
import sys

from PySide6.QtWidgets import QApplication
from PySide6 import QtWidgets
from src.serial.serial_manager import SerialManager
from src.ui.custom.serial_widget import SerialWidget
# ------------------------------ Variable define ------------------------------

# ------------------------------ Function define ------------------------------

def main():
    serial_manager = SerialManager()
    # print("Creating QApplication")
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Windows")) # Fusion style
    print(app.style().name()) # Style name
    try:
        window = SerialWidget(serial_manager)

        window.show()
        app.exec()
    except Exception as e:
        if window:
            window.show_warning(f"Program starting failed:\n{str(e)}")
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(None, "Fatal Error", f"Program starting failed:\n{str(e)}")


if __name__ == "__main__":
    main()
