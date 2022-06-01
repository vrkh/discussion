from PyQt5 import QtWidgets, QtCore, QtGui
import pyautogui
import threading
import ctypes
import socket
import pcinfo
import time
import sys
import ast
import os

username_font = QtGui.QFont()
username_font.setFamily('Segoe UI')
username_font.setPixelSize(14)
translate = QtCore.QCoreApplication.translate

letter_font = QtGui.QFont()
letter_font.setFamily('Segoe UI')
letter_font.setPixelSize(40)
letter_font.setBold(True)

translate = QtCore.QCoreApplication.translate


class SearchUser(QtWidgets.QPushButton):
    def __init__(self, parent: object, x: int, y: int, username: str, color: str) -> None:
        super().__init__(parent)

        self.setGeometry(x, y, 401, 80)
        self.setStyleSheet('QPushButton{\nborder: 1px solid rgb(45, 50, 60);}')

        self.user_letter = QtWidgets.QPushButton(self)
        self.user_letter.setGeometry(10, 10, 60, 60)
        self.user_letter.setStyleSheet('QPushButton{\nbackground-color: rgb%s; border-radius: 30px; color: white; border: none;}' % color)
        self.user_letter.setFont(letter_font)
        self.user_letter.setText(translate('', username[0].upper()))

        self.user_name = QtWidgets.QLabel(self)
        self.user_name.setGeometry(80, 1, 401 - 80, 78)
        self.user_name.setText(translate('', username))
        self.user_name.setFont(username_font)
        self.user_name.setStyleSheet('QLabel{\nborder: none; color: white;}')

    def connect(self, function) -> None:
        self.clicked.connect(function)
        self.user_letter.clicked.connect(function)

    def disconnect(self) -> None:
        self.clicked.disconnect()
        self.user_letter.clicked.disconnect()

    def delete(self) -> None:
        self.deleteLater()


class Message(QtWidgets.QPushButton):
    def __init__(self, parent: object, x: int, y: int, username: str, color: str, messages_counter: int = 0) -> None:
        super().__init__(parent)

        self.messages_counter = messages_counter

        self.setGeometry(x, y, 401, 80)
        self.setStyleSheet('QPushButton{\nborder: 1px solid rgb(45, 50, 60);}')

        self.user_letter = QtWidgets.QPushButton(self)
        self.user_letter.setGeometry(10, 10, 60, 60)
        self.user_letter.setStyleSheet('QPushButton{\nbackground-color: rgb%s; border-radius: 30px; color: white; border: none;}' % color)
        self.user_letter.setFont(letter_font)
        self.user_letter.setText(translate('', username[0].upper()))

        self.user_name = QtWidgets.QLabel(self)
        self.user_name.setGeometry(80, 1, 401 - 80, 78)
        self.user_name.setText(translate('', username))
        self.user_name.setFont(username_font)
        self.user_name.setStyleSheet('QLabel{\nborder: none; color: white;}')

        self.message_counter_button = QtWidgets.QPushButton(self)
        self.message_counter_button.setGeometry(self.width() - 40, 30, 20, 20)
        self.message_counter_button.setStyleSheet('QPushButton{\nbackground-color: rgb(26, 30, 35); border: none; border-radius: 10px; color: white;}')
        self.message_counter_button.setText(translate('', '7'))

        self.message_counter_button.hide()

        if self.messages_counter == 0:
            pass
        elif self.messages_counter < 10:
            self.message_counter_button.setText(translate('', str(self.messages_counter)))
            self.message_counter_button.show()
        else:
            self.message_counter_button.setText(translate('', '9+'))
            self.message_counter_button.show()

    def update_messages_counter(self, message: int) -> None:
        self.messages_counter = message
        if self.messages_counter == 0:
            self.message_counter_button.hide()
        elif self.messages_counter < 10:
            self.message_counter_button.setText(translate('', str(self.messages_counter)))
            self.message_counter_button.show()
        else:
            self.message_counter_button.setText(translate('', '9+'))
            self.message_counter_button.show()

    def connect(self, function) -> None:
        self.clicked.connect(function)
        self.user_letter.clicked.connect(function)
        self.message_counter_button.clicked.connect(function)

    def disconnect(self) -> None:
        self.clicked.disconnect()
        self.user_letter.clicked.disconnect()
        self.message_counter_button.clicked.disconnect()

    def delete(self) -> None:
        self.deleteLater()
