# -*- coding: utf-8 -*-
"""
@File           : serial_widget.py
@Description    : This is a serial widget class file, which will implement
basic serial port gui logic func.
@Author         : CharlesYu
@Created        : 2025/7/14
@Last Modified  : 2025/7/21
"""

# ------------------------------      Import     ------------------------------
# # Really used
from datetime import datetime

from PySide6.QtCore import QTimer, QDateTime, QThread, QMetaObject, Q_ARG, Qt
from PySide6.QtWidgets import QMessageBox, QWidget
from PySide6 import QtGui
from src.ui.designer.serial_widget_ui import Ui_Form
from src.serial import serial_config
from src.serial.serial_manager import SerialManager
from src.app_vars import app_vars
from src.serial.serial_thread import SerialThread
from src.save_to_txt import DataSaveWorker


# ------------------------------ Function define ------------------------------
class SerialWidget(QWidget):
    def __init__(self, serial_manager):
        super().__init__()
        self.ui = Ui_Form()
        self.serial_open = False
        self.serial_receive_hex = False
        self.serial_send_hex = False
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("ui/custom/loonglogo.ico"))

        # serial port
        self.serial_manager = serial_manager

        # Receiving data thread
        self.serial_thread = None

        # A timer to send data to serial port in period.
        self.serial_send_auto_timer = QTimer(self)
        self.serial_send_auto_timer.timeout.connect(self.send_auto_frame)

        # A timer to update serial port recv&send bytes statics in period.
        self.serial_update_1s_timer = QTimer(self)
        self.serial_update_1s_timer.timeout.connect(self.update_per_1s_statics)

        # Saving data thread
        self.save_thread = None
        self.save_worker = None

        # Serial port initialization.
        self.initialize_serial_config_group_box()

        # Serial Port GroupBox
        self.ui.serialPortComboBox.currentTextChanged.connect(self.combo_box_changed)
        self.ui.baudRateComboBox.currentTextChanged.connect(self.combo_box_changed)
        self.ui.byteSizeComboBox.currentTextChanged.connect(self.combo_box_changed)
        self.ui.stopBitsComboBox.currentTextChanged.connect(self.combo_box_changed)
        self.ui.parityComboBox.currentTextChanged.connect(self.combo_box_changed)
        self.ui.serialPortToolButton.clicked.connect(self.refresh_serial_port)
        self.ui.serialOpenPushButton.released.connect(self.switch_serial_state)

        # Receive GroupBox
        self.ui.receiveDataSaveToFileCheckBox.setEnabled(False)
        self.ui.receiveAsciiRadioButton.toggled.connect(self.radio_button_toggled)
        self.ui.receiveHexRadioButton.toggled.connect(self.radio_button_toggled)
        self.ui.receiveClearDataPushButton.clicked.connect(self.clear_rx_data_text_browser)
        self.ui.receiveDataSaveToFileCheckBox.toggled.connect(self.check_box_toggled)

        # receive bytes counts && send bytes counts


        # Send GroupBox
        self.ui.sendSingleLineRadioButton.setEnabled(False)
        self.ui.sendMultipleLineRadioButton.setEnabled(False)
        self.ui.sendAutoCheckBox.setEnabled(False)
        self.ui.sendHexRadioButton.toggled.connect(self.radio_button_toggled)
        self.ui.sendAsciiRadioButton.toggled.connect(self.radio_button_toggled)
        self.ui.sendSingleLineRadioButton.clicked.connect(self.radio_button_toggled)
        self.ui.sendMultipleLineRadioButton.clicked.connect(self.radio_button_toggled)
        self.ui.sendAutoCheckBox.toggled.connect(self.check_box_toggled)

        # Send Stacked Widget
        # # Page 1
        self.ui.sendSingleFramePushButton.setEnabled(False)
        self.ui.sendSingleFramePushButton.clicked.connect(self.send_single_frame_data)
        # # Page 2
        self.ui.sendMultipleFramePushButton_1.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_2.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_3.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_4.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_5.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_6.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_7.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_8.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_9.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_10.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_11.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_12.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_13.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_14.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_15.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_16.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_17.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_18.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_19.clicked.connect(self.send_multiple_frame_data)
        self.ui.sendMultipleFramePushButton_20.clicked.connect(self.send_multiple_frame_data)

    # Serial Port GroupBox
    def refresh_serial_port(self):
        app_vars.port_list, app_vars.port_list_name, app_vars.port_list_info = SerialManager.get_port_info()
        self.ui.serialPortComboBox.clear()
        self.ui.serialPortComboBox.addItems(app_vars.port_list_name)

    def initialize_serial_config_group_box(self):
        self.refresh_serial_port()
        self.ui.baudRateComboBox.addItems(serial_config.BAUDRATE_TEXT_TO_VALUE.keys())
        self.ui.byteSizeComboBox.addItems(serial_config.BYTESIZE_TEXT_TO_VALUE.keys())
        self.ui.stopBitsComboBox.addItems(serial_config.STOPBITS_TEXT_TO_VALUE.keys())
        self.ui.parityComboBox.addItems(serial_config.PARITY_TEXT_TO_VALUE.keys())
        self.ui.baudRateComboBox.setCurrentText(serial_config.BAUDRATE_VALUE_TO_TEXT[115200])
        self.ui.byteSizeComboBox.setCurrentText(serial_config.BYTESIZE_VALUE_TO_TEXT[8])
        self.ui.stopBitsComboBox.setCurrentText(serial_config.STOPBITS_VALUE_TO_TEXT[1])
        self.ui.parityComboBox.setCurrentText(serial_config.PARITY_VALUE_TO_TEXT['N'])
        app_vars.port = self.ui.serialPortComboBox.currentText()
        app_vars.baudrate = serial_config.BAUDRATE_TEXT_TO_VALUE[self.ui.baudRateComboBox.currentText()]
        app_vars.bytesize = serial_config.BYTESIZE_TEXT_TO_VALUE[self.ui.byteSizeComboBox.currentText()]
        app_vars.stopbits = serial_config.STOPBITS_TEXT_TO_VALUE[self.ui.stopBitsComboBox.currentText()]
        app_vars.parity = serial_config.PARITY_TEXT_TO_VALUE[self.ui.parityComboBox.currentText()]
        print(
            f"Initialized port: {app_vars.port} {app_vars.baudrate} {app_vars.bytesize} {app_vars.stopbits} {app_vars.parity}")

    def set_led_label_color(self):
        if self.serial_open:
            self.ui.serialOpenLedLabel.setStyleSheet(f"""
                QLabel {{
                    background-color: red;
                    border-radius: 10px;
            	    border: 2px solid gray;
                    }}
                """)
            self.ui.serialOpenPushButton.setText("打开串口")
        else:
            self.ui.serialOpenLedLabel.setStyleSheet(f"""
                            QLabel {{
                                background-color: green;
                                border-radius: 10px;
            	                border: 2px solid gray;
                                }}
                            """)
            self.ui.serialOpenPushButton.setText("关闭串口")

    def show_error(self, message):
        QMessageBox.critical(self, "Serial port error", message)

    def append_to_text_browser(self, text):
        """
        This is a func, which is used to display data from serial port on receiveDataPlainTextEdit.

        Feature:
        - To display the data from serial thread reading on receiveDataPlainTextEdit.
        - It can stop display, add a timestamp, switch data format.

        Dependent widgets and variables:
        - receiveStopDisplayCheckBox: Check it to pause display.
        - receiveAddTimestampCheckBox: Check it to add a timestamp.
        - serial_receive_hex: True for displaying data in hex format; False for displaying data in ascii format.
        :param text: Data from serial thread.
        :return:
        """
        #lyx,recv bytes update,here
        self.serial_manager.recv_bytes_counts += len(text)

        if not self.ui.receiveStopDisplayCheckBox.isChecked():
            if self.serial_receive_hex:
                text = " ".join(f"{ord(c):02x}" for c in text) + " "
                #print(f"hex: {text}")
            else:
                pass
                #print(f"text: {text}")
            if self.ui.receiveAddTimestampCheckBox.isChecked():
                now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                text = now + ' ' + text
                self.ui.receiveDataPlainTextEdit.appendPlainText(text)
            else:
                self.ui.receiveDataPlainTextEdit.insertPlainText(text)
            if self.save_worker and self.save_worker.is_active():
                #print("Write data to file")
                QMetaObject.invokeMethod(self.save_worker, "write_data", Qt.ConnectionType.QueuedConnection,
                                         Q_ARG(str, text))

    def switch_serial_state(self):
        self.set_led_label_color()
        if self.serial_open:
            try:
                if self.serial_thread:
                    self.serial_thread.stop()
                    self.serial_thread.quit()
                    self.serial_thread.wait()
                    self.serial_thread = None

                self.serial_manager.close()
                self.ui.serialPortToolButton.setEnabled(True)
                self.ui.serialPortComboBox.setEnabled(True)
                self.ui.baudRateComboBox.setEnabled(True)
                self.ui.byteSizeComboBox.setEnabled(True)
                self.ui.stopBitsComboBox.setEnabled(True)
                self.ui.parityComboBox.setEnabled(True)
                self.ui.sendSingleFramePushButton.setEnabled(False)
                self.ui.sendSingleLineRadioButton.setEnabled(False)
                self.ui.sendMultipleLineRadioButton.setEnabled(False)
                self.ui.sendAutoCheckBox.setEnabled(False)
                self.ui.receiveDataSaveToFileCheckBox.setEnabled(False)
                self.serial_open = False
                self.serial_update_1s_timer.stop()
            except Exception as e:
                print(f"Failed to close port: {e}")
        else:
            try:
                self.serial_manager.configure(app_vars.port, app_vars.baudrate, app_vars.bytesize, app_vars.stopbits,
                                              app_vars.parity)
                self.ui.serialPortToolButton.setEnabled(False)
                self.ui.serialPortComboBox.setEnabled(False)
                self.ui.baudRateComboBox.setEnabled(False)
                self.ui.byteSizeComboBox.setEnabled(False)
                self.ui.stopBitsComboBox.setEnabled(False)
                self.ui.parityComboBox.setEnabled(False)
                self.ui.sendSingleFramePushButton.setEnabled(True)
                self.ui.sendSingleLineRadioButton.setEnabled(True)
                self.ui.sendMultipleLineRadioButton.setEnabled(True)
                self.ui.sendAutoCheckBox.setEnabled(True)
                self.ui.receiveDataSaveToFileCheckBox.setEnabled(True)
                self.serial_manager.open()
                self.serial_thread = SerialThread(self.serial_manager.ser)
                self.serial_thread.data_received.connect(self.append_to_text_browser)
                self.serial_thread.error_occurred.connect(self.show_error)
                self.serial_thread.start()
                self.serial_open = True
                self.serial_update_1s_timer.start(1000)    #lyx per 1000ms add for flush statics
            except Exception as e:
                self.show_error(str(e))

    def combo_box_changed(self, text):
        combo = self.sender()
        if combo == self.ui.serialPortComboBox:
            app_vars.port = self.ui.serialPortComboBox.currentText()
            print(f"Port changed to {app_vars.port}")
        elif combo == self.ui.baudRateComboBox:
            app_vars.baudrate = serial_config.BAUDRATE_TEXT_TO_VALUE[self.ui.baudRateComboBox.currentText()]
            print(f"Baudrate changed to {app_vars.baudrate}")
        elif combo == self.ui.byteSizeComboBox:
            app_vars.bytesize = serial_config.BYTESIZE_TEXT_TO_VALUE[self.ui.byteSizeComboBox.currentText()]
            print(f"Bytesize changed to {app_vars.bytesize}")
        elif combo == self.ui.stopBitsComboBox:
            app_vars.stopbits = serial_config.STOPBITS_TEXT_TO_VALUE[self.ui.stopBitsComboBox.currentText()]
            print(f"Stopbits changed to {app_vars.stopbits}")
        elif combo == self.ui.parityComboBox:
            app_vars.parity = serial_config.PARITY_TEXT_TO_VALUE[self.ui.parityComboBox.currentText()]
            print(f"Parity changed to {app_vars.parity}")

    # All radio button
    def radio_button_toggled(self, checked):
        if not checked:
            return
        if self.sender() == self.ui.receiveAsciiRadioButton:
            self.serial_receive_hex = False
        elif self.sender() == self.ui.receiveHexRadioButton:
            self.serial_receive_hex = True
        elif self.sender() == self.ui.sendAsciiRadioButton:
            self.serial_send_hex = False
            hex_text = self.ui.sendSingleFramPlainTextEdit.toPlainText()
            if hex_text:
                print("Switch to ascii display.")
                parts = hex_text.strip().split()
                ascii_text = "".join(chr(int(part, 16)) for part in parts)
                self.ui.sendSingleFramPlainTextEdit.clear()
                self.ui.sendSingleFramPlainTextEdit.insertPlainText(ascii_text)
        elif self.sender() == self.ui.sendHexRadioButton:
            self.serial_send_hex = True
            ascii_text = self.ui.sendSingleFramPlainTextEdit.toPlainText()
            if ascii_text:
                print("Switch to hex display.")
                hex_text = " ".join(f"{ord(c):02x}" for c in ascii_text) + " "
                self.ui.sendSingleFramPlainTextEdit.clear()
                self.ui.sendSingleFramPlainTextEdit.insertPlainText(hex_text)
        elif self.sender() == self.ui.sendSingleLineRadioButton:
            self.ui.sendStackedWidget.setCurrentIndex(0)
            self.ui.sendAutoCheckBox.setEnabled(True)
        elif self.sender() == self.ui.sendMultipleLineRadioButton:
            self.ui.sendStackedWidget.setCurrentIndex(1)
            self.ui.sendAutoCheckBox.setEnabled(False)

    # All check box
    def check_box_toggled(self, checked):
        check_box = self.sender()

        if check_box == self.ui.sendAutoCheckBox:
            if checked:
                try:
                    interval = int(self.ui.sendAutoTimeLineEdit.text())
                    if interval < 10:
                        interval = 10
                    self.ui.sendAutoTimeLineEdit.setEnabled(False)
                    self.serial_send_auto_timer.start(interval)
                    print(f"Serial send auto timer has been started to send data every {interval}ms")
                except ValueError as e:
                    print(f"Failed to start: {e}")
            else:
                self.serial_send_auto_timer.stop()
                self.ui.sendAutoTimeLineEdit.setEnabled(True)
                print(f"Serial send auto timer has been stopped")
        elif check_box == self.ui.receiveDataSaveToFileCheckBox:
            if checked:
                filename = QDateTime.currentDateTime().toString("yyyy_MM_dd_hhmmss") + "_data.txt"
                self.save_thread = QThread()
                self.save_worker = DataSaveWorker(filename)
                self.save_worker.moveToThread(self.save_thread)
                self.save_worker.finished.connect(self.save_thread.quit)
                self.save_thread.finished.connect(self.save_thread.deleteLater)
                self.save_thread.start()
                print(f"File created: {filename}")
            else:
                if self.save_worker:
                    self.save_worker.stop()
                    self.save_thread.quit()
                    self.save_thread.wait()
                    self.save_worker = None
                    self.save_thread = None

    # Receive GroupBox
    def clear_rx_data_text_browser(self):
        self.ui.receiveDataPlainTextEdit.clear()
        self.serial_manager.recv_bytes_counts = 0

    # Send GroupBox
    def send_auto_frame(self):
        text = self.ui.sendSingleFramPlainTextEdit.toPlainText()
        if text:
            self.serial_manager.write_ascii(text)
            #print(f"Auto send data: {text}")

    def update_per_1s_statics(self):
        self.ui.lineEdit_recv_bytes_cnt.setText(str(self.serial_manager.recv_bytes_counts))
        #print("---> recv bytes:",self.serial_manager.recv_bytes_counts)
        self.ui.lineEdit_send_bytes_cnt.setText(str(self.serial_manager.send_bytes_counts))

    # Send Stacked Widget
    # # Page 1: single frame send
    def send_single_frame_data(self):
        if self.serial_open:
            text = self.ui.sendSingleFramPlainTextEdit.toPlainText()
            if self.serial_send_hex:
                parts = text.strip().split()
                # print(f"Current text: {text}")
                hex_data = "".join(chr(int(part, 16)) for part in parts)
                #                 print(f"Send data in hex: {hex_data}")
                self.serial_manager.write_ascii(hex_data)
            else:
                #                 print(f"Send data in ascii: {self.ui.sendSingleFramPlainTextEdit.toPlainText()}")
                self.serial_manager.write_ascii(self.ui.sendSingleFramPlainTextEdit.toPlainText())

    # # Page 2: multiple frames send
    def send_multiple_frame_data(self, checked):
        button = self.sender()

        if self.serial_open:
            if button == self.ui.sendMultipleFramePushButton_1:
                text = self.ui.sendMultipleFrameLineEdit_1.text()
            elif button == self.ui.sendMultipleFramePushButton_2:
                text = self.ui.sendMultipleFrameLineEdit_2.text()
            elif button == self.ui.sendMultipleFramePushButton_3:
                text = self.ui.sendMultipleFrameLineEdit_3.text()
            elif button == self.ui.sendMultipleFramePushButton_4:
                text = self.ui.sendMultipleFrameLineEdit_4.text()
            elif button == self.ui.sendMultipleFramePushButton_5:
                text = self.ui.sendMultipleFrameLineEdit_5.text()
            elif button == self.ui.sendMultipleFramePushButton_6:
                text = self.ui.sendMultipleFrameLineEdit_6.text()
            elif button == self.ui.sendMultipleFramePushButton_7:
                text = self.ui.sendMultipleFrameLineEdit_7.text()
            elif button == self.ui.sendMultipleFramePushButton_8:
                text = self.ui.sendMultipleFrameLineEdit_8.text()
            elif button == self.ui.sendMultipleFramePushButton_9:
                text = self.ui.sendMultipleFrameLineEdit_9.text()
            elif button == self.ui.sendMultipleFramePushButton_10:
                text = self.ui.sendMultipleFrameLineEdit_10.text()
            elif button == self.ui.sendMultipleFramePushButton_11:
                text = self.ui.sendMultipleFrameLineEdit_11.text()
            elif button == self.ui.sendMultipleFramePushButton_12:
                text = self.ui.sendMultipleFrameLineEdit_12.text()
            elif button == self.ui.sendMultipleFramePushButton_13:
                text = self.ui.sendMultipleFrameLineEdit_13.text()
            elif button == self.ui.sendMultipleFramePushButton_14:
                text = self.ui.sendMultipleFrameLineEdit_14.text()
            elif button == self.ui.sendMultipleFramePushButton_15:
                text = self.ui.sendMultipleFrameLineEdit_15.text()
            elif button == self.ui.sendMultipleFramePushButton_16:
                text = self.ui.sendMultipleFrameLineEdit_16.text()
            elif button == self.ui.sendMultipleFramePushButton_17:
                text = self.ui.sendMultipleFrameLineEdit_17.text()
            elif button == self.ui.sendMultipleFramePushButton_18:
                text = self.ui.sendMultipleFrameLineEdit_18.text()
            elif button == self.ui.sendMultipleFramePushButton_19:
                text = self.ui.sendMultipleFrameLineEdit_19.text()
            elif button == self.ui.sendMultipleFramePushButton_20:
                text = self.ui.sendMultipleFrameLineEdit_20.text()
            if self.serial_send_hex:
                parts = text.strip().split()
                hex_data = "".join(chr(int(part, 16)) for part in parts)
                self.serial_manager.write_ascii(hex_data)
            else:
                self.serial_manager.write_ascii(text)

    def closeEvent(self, event):
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread.quit()
            self.serial_thread.wait()
        if self.serial_manager.is_open:
            self.serial_manager.close()
        super().closeEvent(event)


# serial_manager = SerialManager()
#
# app = QApplication(sys.argv)
# window = SerialWidget(serial_manager)
# window.show()
# app.exec()
