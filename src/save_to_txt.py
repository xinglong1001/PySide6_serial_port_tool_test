# -*- coding: utf-8 -*-
"""
@File           : save_to_txt.py
@Description    : This is used for saving temperature data.
@Author         : CharlesYu
@Created        : 2025/7/18
@Last Modified  : 2025/7/18
"""
# ------------------------------      Import     ------------------------------
import  os
from datetime import datetime
from PySide6.QtCore import QObject, Signal, Slot
# ------------------------------ Variable define ------------------------------

# ------------------------------ Function define ------------------------------
class DataSaveWorker(QObject):
    finished = Signal()

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self._active = True
        self.file = open(filename, "a", encoding="utf-8")

    @Slot(str)
    def write_data(self, data: str):
        if self._active:
            self.file.write(data + "\n")  # UTF-8 will automatically convert line breaks depending on the system.
            self.file.flush()

    @Slot()
    def stop(self):
        self._active = False
        if self.file:
            self.file.close()
        self.finished.emit()

    def is_active(self):
        return self._active
