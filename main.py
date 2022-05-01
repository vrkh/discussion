from PyQt5 import QtWidgets, QtCore, QtGui
import multiprocessing
import threading
import pyautogui
import ctypes
import socket
import sys
import os

# Custom Widgets
from custombuttons import MainButton
from windowhint import WindowHint

WINDOW_GEOMETRY = (700, 500)
HINT_HEIGHT = 25
HINT_BUTTON_WIDTH = 40

SECTIONS_FONT = QtGui.QFont()
SECTIONS_FONT.setFamily('Segoe UI')
SECTIONS_FONT.setPointSize(20)

LINEEDIT_FONT = QtGui.QFont()
LINEEDIT_FONT.setFamily('Segoe UI')
LINEEDIT_FONT.setPointSize(14)

CHECKBOX_FONT = QtGui.QFont()
CHECKBOX_FONT.setFamily('Segoe UI')
CHECKBOX_FONT.setPointSize(10)


class MainWindow(QtWidgets.QMainWindow):

    ##################################################
    # Animations                                     #
    ##################################################

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

    ##################################################
    # Functions                                      #
    ##################################################

    def authorize(self) -> None:
        print('auth')
        self.fade(self.authorize_frame, 300)
        self.unfade(self.authorize_frame, 500)

    def show_regisration_frame(self) -> None:
        self.fade(self.authorize_frame, 300)

        self.fade(self.registration_frame, 0)
        self.registration_frame.show()
        self.unfade(self.registration_frame, 300)
        self.authorize_frame.hide()

    def show_login_frame(self) -> None:
        self.fade(self.registration_frame, 300)

        self.fade(self.authorize_frame, 0)
        self.authorize_frame.show()
        self.unfade(self.authorize_frame, 300)
        self.registration_frame.hide()

    def remember_me(self) -> None:
        if self.remember_me_checkbox.isChecked():
            self.remember_me_checkbox.setStyleSheet('QCheckBox{\ncolor: white;}QCheckBox::indicator { width: 15px; height: 15px; background-color: rgb(0, 170, 107); border-radius: 3px;}')
        else:
            self.remember_me_checkbox.setStyleSheet('QCheckBox{\ncolor: white;}QCheckBox::indicator { width: 15px; height: 15px; background-color: rgb(30, 30, 30); border-radius: 3px;}')

    # def resizeEvent(self, event) -> None:
    #     print(f"resize event")
    #     QtWidgets.QMainWindow.resizeEvent(self, event)

    def close_window(self) -> None:
        print('close')
        self.close()
        application_is_running.value = 0

    def minimize_window(self) -> None:
        print('minimize')
        self.showMinimized()

    def hide_window(self) -> None:
        print('hide')
        self.hide()

    def __init__(self) -> None:
        super().__init__()

        self._translate = QtCore.QCoreApplication.translate
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet('QMainWindow{\nbackground-color: rgb(20, 20, 20);}')
        self.setGeometry((pyautogui.size()[0] // 2) - (WINDOW_GEOMETRY[0] // 2), (pyautogui.size()[1] // 2) - (WINDOW_GEOMETRY[1] // 2), WINDOW_GEOMETRY[0], WINDOW_GEOMETRY[1])

        ##################################################
        # Window hint                                    #
        ##################################################

        self.window_hint = WindowHint(self, HINT_HEIGHT, (15, 15, 15), HINT_BUTTON_WIDTH)

        self.window_hint.setButton(self.close_window)
        self.window_hint.setButtonText('🞩', ('Segoe UI', 14))
        self.window_hint.setButtonStyles('QPushButton{\ncolor: white; background-color: rgb(15, 15, 15); border-radius: 0px;}QPushButton:hover{\nbackground-color: rgb(255, 30, 30);}')

        self.window_hint.setButton(self.minimize_window)
        self.window_hint.setButtonText('▭', ('Segoe UI', 20))
        self.window_hint.setButtonStyles('QPushButton{\ncolor: white; background-color: rgb(15, 15, 15); border-radius: 0px;}QPushButton:hover{\nbackground-color: rgb(40, 40, 40);}')

        self.window_hint.setButton(self.hide_window)
        self.window_hint.setButtonText('⎯', ('Segoe UI', 12))
        self.window_hint.setButtonStyles('QPushButton{\ncolor: white; background-color: rgb(15, 15, 15); border-radius: 0px;}QPushButton:hover{\nbackground-color: rgb(40, 40, 40);}')

        ##################################################
        # Logging in                                     #
        ##################################################

        # Authorize

        self.authorize_frame = QtWidgets.QFrame(self)
        self.authorize_frame.setGeometry(0, HINT_HEIGHT, WINDOW_GEOMETRY[0], WINDOW_GEOMETRY[1] - HINT_HEIGHT)
        self.authorize_frame.setStyleSheet('QFrame{\nbackground-color: rgb(20, 20, 20);}')

        self.authorize_label = QtWidgets.QLabel(self.authorize_frame)
        self.authorize_label.setGeometry(0, 20 + HINT_HEIGHT, WINDOW_GEOMETRY[0], 40)
        self.authorize_label.setStyleSheet('QLabel{\ncolor: white;}')
        self.authorize_label.setAlignment(QtCore.Qt.AlignCenter)
        self.authorize_label.setFont(SECTIONS_FONT)
        self.authorize_label.setText(self._translate("authorize", "АВТОРИЗАЦИЯ"))

        self.login_lineedit = QtWidgets.QLineEdit(self.authorize_frame)
        self.login_lineedit.setGeometry(WINDOW_GEOMETRY[0] // 4, self.authorize_label.y() + 40, WINDOW_GEOMETRY[0] // 2, 40)
        self.login_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); border: none; border-bottom: 2px solid rgb(255, 255, 255); color: white}')
        self.login_lineedit.setFont(LINEEDIT_FONT)
        self.login_lineedit.setPlaceholderText('Логин')

        self.password_lineedit = QtWidgets.QLineEdit(self.authorize_frame)
        self.password_lineedit.setGeometry(WINDOW_GEOMETRY[0] // 4, self.authorize_label.y() + 110, WINDOW_GEOMETRY[0] // 2, 40)
        self.password_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); border: none; border-bottom: 2px solid rgb(255, 255, 255); color: white}')
        self.password_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineedit.setFont(LINEEDIT_FONT)
        self.password_lineedit.setPlaceholderText('Пароль')

        self.remember_me_checkbox = QtWidgets.QCheckBox(self.authorize_frame)
        self.remember_me_checkbox.setGeometry(WINDOW_GEOMETRY[0] // 4, self.authorize_label.y() + 180, WINDOW_GEOMETRY[0] // 2, 40)
        self.remember_me_checkbox.setStyleSheet('QCheckBox{\ncolor: white;}QCheckBox::indicator { width: 15px; height: 15px; background-color: rgb(30, 30, 30); border-radius: 3px;}')
        self.remember_me_checkbox.setText(self._translate('Remember me', 'Запомнить меня'))
        self.remember_me_checkbox.setFont(CHECKBOX_FONT)
        self.remember_me_checkbox.stateChanged.connect(self.remember_me)

        self.authorize_button = MainButton(self.authorize_frame, WINDOW_GEOMETRY[0] // 2, self.authorize_label.y() + 185, WINDOW_GEOMETRY[0] // 4, 30, '#1e1e1e', '#00aa6c', '#ffffff', '#ffffff', 100)
        self.authorize_button.setFont(CHECKBOX_FONT)
        self.authorize_button.setText(self._translate('Authorize', 'Авторизоваться'))
        self.authorize_button.clicked.connect(self.authorize)

        self.forget_password = QtWidgets.QPushButton(self.authorize_frame)
        self.forget_password.setGeometry(WINDOW_GEOMETRY[0] // 3, self.authorize_frame.height() - 150, WINDOW_GEOMETRY[0] // 3, 25)
        self.forget_password.setFont(CHECKBOX_FONT)
        self.forget_password.setStyleSheet('QPushButton{\nbackground-color: rgb(20, 20, 20); border-radius: 0px; color: rgb(0, 170, 107);}')
        self.forget_password.setText(self._translate('Forger', 'Сбросить пароль'))
        self.forget_password.clicked.connect(self.authorize)

        self.register_account = QtWidgets.QPushButton(self.authorize_frame)
        self.register_account.setGeometry(WINDOW_GEOMETRY[0] // 3, self.authorize_frame.height() - 120, WINDOW_GEOMETRY[0] // 3, 25)
        self.register_account.setFont(CHECKBOX_FONT)
        self.register_account.setStyleSheet('QPushButton{\nbackground-color: rgb(20, 20, 20); border-radius: 0px; color: rgb(0, 170, 107)}')
        self.register_account.setText(self._translate('Registrate', 'Зарегистрироваться'))
        self.register_account.clicked.connect(self.show_regisration_frame)

        # Forgot password

        self.registration_frame = QtWidgets.QFrame(self)
        self.registration_frame.setGeometry(0, HINT_HEIGHT, WINDOW_GEOMETRY[0], WINDOW_GEOMETRY[1] - HINT_HEIGHT)
        self.registration_frame.setStyleSheet('QFrame{\nbackground-color: rgb(20, 20, 20);}')

        self.registration_label = QtWidgets.QLabel(self.registration_frame)
        self.registration_label.setGeometry(0, 20 + HINT_HEIGHT, WINDOW_GEOMETRY[0], 40)
        self.registration_label.setStyleSheet('QLabel{\ncolor: white;}')
        self.registration_label.setAlignment(QtCore.Qt.AlignCenter)
        self.registration_label.setFont(SECTIONS_FONT)
        self.registration_label.setText(self._translate("Registrate", "РЕГИСТРАЦИЯ"))

        self.registration_email_lineedit = QtWidgets.QLineEdit(self.registration_frame)
        self.registration_email_lineedit.setGeometry(WINDOW_GEOMETRY[0] // 4, self.authorize_label.y() + 40, WINDOW_GEOMETRY[0] // 2, 40)
        self.registration_email_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); border: none; border-bottom: 2px solid rgb(255, 255, 255); color: white}')
        self.registration_email_lineedit.setFont(LINEEDIT_FONT)
        self.registration_email_lineedit.setPlaceholderText('Почта')

        self.registation_login_lineedit = QtWidgets.QLineEdit(self.registration_frame)
        self.registation_login_lineedit.setGeometry(WINDOW_GEOMETRY[0] // 4, self.authorize_label.y() + 110, WINDOW_GEOMETRY[0] // 2, 40)
        self.registation_login_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); border: none; border-bottom: 2px solid rgb(255, 255, 255); color: white}')
        self.registation_login_lineedit.setFont(LINEEDIT_FONT)
        self.registation_login_lineedit.setPlaceholderText('Логин')

        self.registation_password_lineedit = QtWidgets.QLineEdit(self.registration_frame)
        self.registation_password_lineedit.setGeometry(WINDOW_GEOMETRY[0] // 4, self.authorize_label.y() + 180, WINDOW_GEOMETRY[0] // 2, 40)
        self.registation_password_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); border: none; border-bottom: 2px solid rgb(255, 255, 255); color: white}')
        self.registation_password_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.registation_password_lineedit.setFont(LINEEDIT_FONT)
        self.registation_password_lineedit.setPlaceholderText('Пароль')

        self.already_have_account = QtWidgets.QPushButton(self.registration_frame)
        self.already_have_account.setGeometry(WINDOW_GEOMETRY[0] // 3, self.authorize_frame.height() - 120, WINDOW_GEOMETRY[0] // 3, 25)
        self.already_have_account.setFont(CHECKBOX_FONT)
        self.already_have_account.setStyleSheet('QPushButton{\nbackground-color: rgb(20, 20, 20); border-radius: 0px; color: rgb(0, 170, 107)}')
        self.already_have_account.setText(self._translate('Already have', 'У меня уже есть аккаунт'))
        self.already_have_account.clicked.connect(self.show_login_frame)

        self.registration_button = MainButton(self.registration_frame, WINDOW_GEOMETRY[0] // 3, self.authorize_label.y() + 255, WINDOW_GEOMETRY[0] // 3, 30, '#1e1e1e', '#00aa6c', '#ffffff', '#ffffff', 100)
        self.registration_button.setFont(CHECKBOX_FONT)
        self.registration_button.setText(self._translate('Registrate', 'Зарегистрироваться'))
        self.registration_button.clicked.connect(self.authorize)

        self.registration_frame.hide()


global APPDATA_DIRECTORY, application_is_running
APPDATA_DIRECTORY = os.getenv('APPDATA')
application_is_running = multiprocessing.Value(ctypes.c_int16, 1)

##################################################
# Socket server                                  #
##################################################


def socket_server() -> None:
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('178.250.158.150', 1337))

    while application_is_running.value:
        server_data = client.recv(65536)
        if server_data:
            print(server_data.decode('utf-8'))


# Strart server in extra thread
threading.Thread(target=socket_server).start()

application = QtWidgets.QApplication(sys.argv)
messanger_window = MainWindow()
messanger_window.show()
application.exec()
