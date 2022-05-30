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

# Custom widgets
from windowhint import WindowHint

translate = QtCore.QCoreApplication.translate

section_font = QtGui.QFont()
section_font.setPixelSize(18)
section_font.setFamily('Segoe UI')

lineedit_title_font = QtGui.QFont()
lineedit_title_font.setPixelSize(12)
lineedit_title_font.setFamily('Segoe UI')

lineedit_font = QtGui.QFont()
lineedit_font.setPixelSize(15)
lineedit_font.setFamily('Segoe UI')


class MainWindow(QtWidgets.QMainWindow):
    # Animations
    def fade(self, widget: object, duration: int) -> None:
        self.effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(duration)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def unfade(self, widget: object, duration: int) -> None:
        self.effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(duration)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    # Open Registration frame
    def show_registration_frame(self):

        self.registration_frame.hide()
        self.fade(self.registration_frame, 0)

        self.auth_frame.hide()
        self.registration_frame.show()
        self.unfade(self.registration_frame, 300)

    # Openg auth frame
    def show_auth_frame(self):

        self.auth_frame.hide()
        self.fade(self.auth_frame, 0)

        self.registration_frame.hide()
        self.auth_frame.show()
        self.unfade(self.auth_frame, 300)

    def show_registration_code_frame(self):
        pass

    def __init__(self) -> None:
        super().__init__()

        # Window settings
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(SCREEN_RESOLUTION[0] // 2 - AUTH_WINDOW_SIZE[0] // 2, SCREEN_RESOLUTION[1] // 2 - AUTH_WINDOW_SIZE[1] // 2, AUTH_WINDOW_SIZE[0], AUTH_WINDOW_SIZE[1])
        self.setStyleSheet('QMainWindow{\nbackground-color: rgb%s;}' % str(WINDOW_BACK_COLOR))

        # Window hint
        self.auth_window_hint = WindowHint(self, HINT_HEIGHT, (5, 5, 5), 40)

        self.auth_window_hint.setButton(lambda: self.close())
        self.auth_window_hint.setButtonText('🞩', ('Segoe UI', 21))
        self.auth_window_hint.setButtonStyles('QPushButton{\ncolor: white; background-color: rgb(5, 5, 5); border-radius: 0px;}QPushButton:hover{\nbackground-color: rgb(255, 30, 30);}')

        self.auth_window_hint.setButton(lambda: self.showMinimized())
        self.auth_window_hint.setButtonText('⎯', ('Segoe UI', 18))
        self.auth_window_hint.setButtonStyles('QPushButton{\ncolor: white; background-color: rgb(5, 5, 5); border-radius: 0px;}QPushButton:hover{\nbackground-color: rgb(20, 20, 20);}')

        # Window settings
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(SCREEN_RESOLUTION[0] // 2 - AUTH_WINDOW_SIZE[0] // 2, SCREEN_RESOLUTION[1] // 2 - AUTH_WINDOW_SIZE[1] // 2, AUTH_WINDOW_SIZE[0], AUTH_WINDOW_SIZE[1])
        self.setStyleSheet('QMainWindow{\nbackground-color: rgb(%s);}' % WINDOW_BACK_COLOR)

        # Window hint
        self.auth_window_hint = WindowHint(self, HINT_HEIGHT, (5, 5, 5), 40)

        self.auth_window_hint.setButton(lambda: self.close())
        self.auth_window_hint.setButtonText('🞩', ('Segoe UI', 21))
        self.auth_window_hint.setButtonStyles('QPushButton{\ncolor: white; background-color: rgb(5, 5, 5); border-radius: 0px;}QPushButton:hover{\nbackground-color: rgb(255, 30, 30);}')

        self.auth_window_hint.setButton(lambda: self.showMinimized())
        self.auth_window_hint.setButtonText('⎯', ('Segoe UI', 18))
        self.auth_window_hint.setButtonStyles('QPushButton{\ncolor: white; background-color: rgb(5, 5, 5); border-radius: 0px;}QPushButton:hover{\nbackground-color: rgb(20, 20, 20);}')

        # Auth Frame
        self.auth_frame = QtWidgets.QFrame(self)
        self.auth_frame.setGeometry(0, HINT_HEIGHT, self.width(), self.height() - HINT_HEIGHT)
        self.auth_frame.setStyleSheet('QMainWindow{\nbackground-color: rgb%s;}' % str(WINDOW_BACK_COLOR))

        self.auth_label = QtWidgets.QLabel(self.auth_frame)
        self.auth_label.setGeometry(self.auth_frame.width() // 6, 40, self.auth_frame.width() // 6 * 4, 40)
        self.auth_label.setStyleSheet('QLabel{\ncolor: white;}')
        self.auth_label.setText(translate('', 'Авторизация'))
        self.auth_label.setFont(section_font)

        self.auth_lineedit_label = QtWidgets.QLabel(self.auth_frame)
        self.auth_lineedit_label.setGeometry(self.auth_frame.width() // 6, 95, self.auth_frame.width() // 6 * 4, 20)
        self.auth_lineedit_label.setStyleSheet('QLabel{\ncolor: white;}')
        self.auth_lineedit_label.setText(translate('', 'Логин'))
        self.auth_lineedit_label.setFont(lineedit_title_font)

        self.auth_lineedit = QtWidgets.QLineEdit(self.auth_frame)
        self.auth_lineedit.setGeometry(self.auth_frame.width() // 6, 110, self.auth_frame.width() // 6 * 4, 40)
        self.auth_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); color: white; border: none; border-bottom: 2px solid white;}')
        self.auth_lineedit.setFont(lineedit_font)

        self.password_lineedit_label = QtWidgets.QLabel(self.auth_frame)
        self.password_lineedit_label.setGeometry(self.auth_frame.width() // 6, 185, self.auth_frame.width() // 6 * 4, 20)
        self.password_lineedit_label.setStyleSheet('QLabel{\ncolor: white;}')
        self.password_lineedit_label.setText(translate('', 'Пароль'))
        self.password_lineedit_label.setFont(lineedit_title_font)

        self.password_lineedit = QtWidgets.QLineEdit(self.auth_frame)
        self.password_lineedit.setGeometry(self.auth_frame.width() // 6, 200, self.auth_frame.width() // 6 * 4, 40)
        self.password_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); color: white; border: none; border-bottom: 2px solid white;}')
        self.password_lineedit.setFont(lineedit_font)
        self.password_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.remember_me = QtWidgets.QCheckBox(self.auth_frame)
        self.remember_me.setGeometry(self.auth_frame.width() // 6, 240, self.auth_frame.width() // 6 * 4, 40)
        self.remember_me.setText(translate('', 'Запомнить меня'))
        self.remember_me.setStyleSheet('QCheckBox{\ncolor: white; margin-bottom: 6px;}')
        self.remember_me.setFont(lineedit_title_font)

        self.login_button = QtWidgets.QPushButton(self.auth_frame)
        self.login_button.setGeometry(self.auth_frame.width() // 6, 280, self.auth_frame.width() // 6 * 2 - 5, 40)
        self.login_button.setStyleSheet('QPushButton{\nborder-radius: 6px; background-color: rgb(6, 17, 185); color: white;}')
        self.login_button.setText(translate('', 'Авторизация'))
        self.login_button.setFont(lineedit_title_font)

        self.registration_button = QtWidgets.QPushButton(self.auth_frame)
        self.registration_button.setGeometry(self.auth_frame.width() // 6 * 3 + 5, 280, self.auth_frame.width() // 6 * 2 - 5, 40)
        self.registration_button.setStyleSheet('QPushButton{\nborder-radius: 6px; background-color: rgb(5, 5, 5); border: 1px solid rgb(6, 17, 185); color: rgb(6, 17, 185);}')
        self.registration_button.setText(translate('', 'Регистрация'))
        self.registration_button.setFont(lineedit_title_font)
        self.registration_button.clicked.connect(self.show_registration_frame)

        # Registration frame
        self.registration_frame = QtWidgets.QFrame(self)
        self.registration_frame.setGeometry(0, HINT_HEIGHT, self.width(), self.height() - HINT_HEIGHT)
        self.registration_frame.setStyleSheet('QMainWindow{\nbackground-color: rgb(%s);}' % WINDOW_BACK_COLOR)

        self.registration_label = QtWidgets.QLabel(self.registration_frame)
        self.registration_label.setGeometry(self.registration_frame.width() // 6, 40, self.registration_frame.width() // 6 * 4, 40)
        self.registration_label.setStyleSheet('QLabel{\ncolor: white;}')
        self.registration_label.setText(translate('', 'Регистрация'))
        self.registration_label.setFont(section_font)

        self.registration_lineedit_label = QtWidgets.QLabel(self.registration_frame)
        self.registration_lineedit_label.setGeometry(self.registration_frame.width() // 6, 95, self.registration_frame.width() // 6 * 4, 20)
        self.registration_lineedit_label.setStyleSheet('QLabel{\ncolor: white;}')
        self.registration_lineedit_label.setText(translate('', 'email'))
        self.registration_lineedit_label.setFont(lineedit_title_font)

        self.registration_lineedit = QtWidgets.QLineEdit(self.registration_frame)
        self.registration_lineedit.setGeometry(self.registration_frame.width() // 6, 110, self.registration_frame.width() // 6 * 4, 40)
        self.registration_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); color: white; border: none; border-bottom: 2px solid white;}')
        self.registration_lineedit.setFont(lineedit_font)

        self.registration_login_lineedit_label = QtWidgets.QLabel(self.registration_frame)
        self.registration_login_lineedit_label.setGeometry(self.registration_frame.width() // 6, 185, self.registration_frame.width() // 6 * 4, 20)
        self.registration_login_lineedit_label.setStyleSheet('QLabel{\ncolor: white;}')
        self.registration_login_lineedit_label.setText(translate('', 'Логин'))
        self.registration_login_lineedit_label.setFont(lineedit_title_font)

        self.registration_login_lineedit = QtWidgets.QLineEdit(self.registration_frame)
        self.registration_login_lineedit.setGeometry(self.registration_frame.width() // 6, 200, self.registration_frame.width() // 6 * 4, 40)
        self.registration_login_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); color: white; border: none; border-bottom: 2px solid white;}')
        self.registration_login_lineedit.setFont(lineedit_font)

        self.registration_password_lineedit_label = QtWidgets.QLabel(self.registration_frame)
        self.registration_password_lineedit_label.setGeometry(self.registration_frame.width() // 6, 275, self.registration_frame.width() // 6 * 4, 20)
        self.registration_password_lineedit_label.setStyleSheet('QLabel{\ncolor: white;}')
        self.registration_password_lineedit_label.setText(translate('', 'Пароль'))
        self.registration_password_lineedit_label.setFont(lineedit_title_font)

        self.registration_password_lineedit = QtWidgets.QLineEdit(self.registration_frame)
        self.registration_password_lineedit.setGeometry(self.registration_frame.width() // 6, 290, self.registration_frame.width() // 6 * 4, 40)
        self.registration_password_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); color: white; border: none; border-bottom: 2px solid white;}')
        self.registration_password_lineedit.setFont(lineedit_font)
        self.registration_password_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.registation_registration_button = QtWidgets.QPushButton(self.registration_frame)
        self.registation_registration_button.setGeometry(self.registration_frame.width() // 6, 350, self.registration_frame.width() // 6 * 2 - 5, 40)
        self.registation_registration_button.setStyleSheet('QPushButton{\nborder-radius: 6px; background-color: rgb(6, 17, 185); color: white;}')
        self.registation_registration_button.setText(translate('', 'Регистрация'))
        self.registation_registration_button.setFont(lineedit_title_font)

        self.registation_login_button = QtWidgets.QPushButton(self.registration_frame)
        self.registation_login_button.setGeometry(self.registration_frame.width() // 6 * 3 + 5, 350, self.registration_frame.width() // 6 * 2 - 5, 40)
        self.registation_login_button.setStyleSheet('QPushButton{\nborder-radius: 6px; background-color: rgb(5, 5, 5); border: 1px solid rgb(6, 17, 185); color: rgb(6, 17, 185);}')
        self.registation_login_button.setText(translate('', 'Автоизация'))
        self.registation_login_button.setFont(lineedit_title_font)
        self.registation_login_button.clicked.connect(self.show_auth_frame)

        self.registration_frame.hide()

        # Registration code frame
        self.registration_code_frame = QtWidgets.QFrame(self)
        self.registration_code_frame.setGeometry(0, HINT_HEIGHT, self.width(), self.height() - HINT_HEIGHT)
        self.registration_code_frame.setStyleSheet('QFrame{\nbackground-color: rgb(%s);}' % WINDOW_BACK_COLOR)

        self.registration_code_label = QtWidgets.QLabel(self.registration_code_frame)
        self.registration_code_label.setGeometry(self.registration_code_frame.width() // 6, 185, self.registration_code_frame.width() // 6 * 4, 20)
        self.registration_code_label.setStyleSheet('QLabel{\ncolor: white;}')
        self.registration_code_label.setText(translate('', 'Ключ с email'))
        self.registration_code_label.setFont(lineedit_title_font)

        self.registration_code_lineedit = QtWidgets.QLineEdit(self.registration_code_frame)
        self.registration_code_lineedit.setGeometry(self.registration_code_frame.width() // 6, 200, self.registration_code_frame.width() // 6 * 4, 40)
        self.registration_code_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); color: white; border: none; border-bottom: 2px solid white;}')
        self.registration_code_lineedit.setFont(lineedit_font)

        self.registation_registration_button = QtWidgets.QPushButton(self.registration_code_frame)
        self.registation_registration_button.setGeometry(self.registration_code_frame.width() // 6, 260, self.registration_code_frame.width() - 115, 40)
        self.registation_registration_button.setStyleSheet('QPushButton{\nborder-radius: 6px; background-color: rgb(6, 17, 185); color: white;}')
        self.registation_registration_button.setText(translate('', 'Регистрация'))
        self.registation_registration_button.setFont(lineedit_title_font)

        self.registration_code_frame.hide()


AUTH_WINDOW_SIZE = 350, 500
HINT_HEIGHT = 25
WINDOW_BACK_COLOR = '5, 5, 5'
SCREEN_RESOLUTION = pyautogui.size()
APPDATA_PATH = os.getenv('APPDATA')


# Server
def start_server():
    global server

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('178.250.158.150', 7070))

    while True:
        server_data = server.recv(4096).decode('utf-8')
        if server_data:
            print('[SERVER]:', server_data)

            if server_data == 'stop':
                break


application = QtWidgets.QApplication(sys.argv)
messanger_window = MainWindow()
threading.Thread(target=start_server).start()
messanger_window.show()
application.exec()
