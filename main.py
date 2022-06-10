from email import message
import multiprocessing
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.style import use
import pyautogui
import threading
import ctypes
import socket
import random
import sys
import ast
import os

# Custom widgets
from windowhint import WindowHint
from messengerwidgets import SearchUser, Message

translate = QtCore.QCoreApplication.translate


AUTH_WINDOW_SIZE = 350, 500
HINT_HEIGHT = 25
WINDOW_BACK_COLOR = '5, 5, 5'
SCREEN_RESOLUTION = pyautogui.size()
APPDATA_PATH = os.getenv('APPDATA')
password = ''
username = ''
getter = ''
search_users_list = []


MESSENGER_WINDOW_SIZE = 1100, 600
SEARCH_USERS_LIST = multiprocessing.Array(ctypes.c_char_p, 500)
MESSAGE_USERS_LIST = multiprocessing.Array(ctypes.c_char_p, 500)

section_font = QtGui.QFont()
section_font.setPixelSize(18)
section_font.setFamily('Segoe UI')

lineedit_title_font = QtGui.QFont()
lineedit_title_font.setPixelSize(12)
lineedit_title_font.setFamily('Segoe UI')

lineedit_font = QtGui.QFont()
lineedit_font.setPixelSize(15)
lineedit_font.setFamily('Segoe UI')


def encode_chars(message):
    message_array = []
    for char in message:
        message_array.append(ord(char))
    return message_array


def decode_chars(message_array):
    message = ''
    for char in message_array:
        message += chr(char)
    return message


def send_message(sender, getter, message):
    if len(message) <= 100:
        if getter:
            server.send(f'message ["{sender}","{getter}"] {encode_chars(message)}'.encode())
        else:
            ctypes.windll.user32.MessageBoxW(0, f'Получатель не выбран.', 'Ошибка', 0x10)
    else:
        ctypes.windll.user32.MessageBoxW(0, f'Максимальная длина сообщения - 100.\nВаше сообщение содержит {len(message)} символов.', 'Ошибка', 0x10)


# Start frame logic
def try_to_registrate() -> None:
    global server
    error_list = ''
    registration_login = messanger_window.registration_login_lineedit.text()
    registration_password = messanger_window.registration_password_lineedit.text()

    if len(registration_login) < 5:
        error_list += 'Введенный логин слишком короткий. (минимум 5 симв.)\n'
    if ' ' in registration_login:
        error_list += 'Логин не должен содержать пробелов в себе.'
    if len(registration_password) < 5:
        error_list += 'Введенный пароль слишком короткой. (минимум 5 симв.)\n'
    if ' ' in registration_password:
        error_list += 'Пароль не должен содержать пробелов в себе.'

    # Some type of error
    if error_list:
        ctypes.windll.user32.MessageBoxW(0, error_list, 'Ошибка', 0x10)
    else:
        pass
        server.send(f'trytoreg {registration_login} {registration_password}'.encode())


def try_to_auth() -> None:
    global server
    global username
    global password

    error_list = ''
    input_login = messanger_window.auth_lineedit.text()
    input_password = messanger_window.password_lineedit.text()

    if len(input_login) < 5:
        error_list += 'Введенный логин слишком короткий. (минимум 5 симв.)\n'
    if ' ' in input_login:
        error_list += 'Логин не может содержать пробелов в себе.'
    if len(input_password) < 5:
        error_list += 'Введенный пароль слишком короткой. (минимум 5 симв.)\n'
    if ' ' in input_password:
        error_list += 'Пароль не может содержать пробелов в себе.'

    if not error_list:
        server.send(f'trytoauth {input_login} {input_password}'.encode())


def set_getter(value):
    global getter
    global search_users_list
    getter = search_users_list[value].user_name.text()
    print(username, getter)
    window.message_title_frame.setText(translate('', getter))


class MainWindow(QtWidgets.QWidget):
    global SEARCH_USERS_LIST
    global MESSAGE_USERS_LIST
    global server
    global username
    global set_getter
    global search_users_list

    # Messenger logic

    def show_messages(self):
        for item in search_users_list:
            item.hide()

        self.search_button.setStyleSheet('QPushButton{\nbackground-image: url(images/magnifier.png); border: none;}')
        self.search_button.clicked.disconnect()
        self.search_button.clicked.connect(self.search_for_users)

    def search_for_users(self):

        server.send('userslist'.encode())
        while not list(SEARCH_USERS_LIST)[0]:
            pass
        else:
            self.search_button.setStyleSheet('QPushButton{\nbackground-image: url(images/cross.png); border: none;}')
            self.search_button.clicked.disconnect()
            self.search_button.clicked.connect(self.show_messages)

            for user in list(SEARCH_USERS_LIST):
                if user:
                    if window.search_lineedit.text() in user.decode():
                        window.messages_container.addWidget(SearchUser(user.decode(), f'({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})'))
                else:
                    break
            users = [window.messages_container.itemAt(i).widget() for i in range(1, window.messages_container.count())]
            search_users_list.extend(users)

            for i in range(len(search_users_list)):
                exec(f"search_users_list[{i}].clicked.connect(lambda: set_getter({i}))")

            # Cleaning up the Search user list
            for i in range(500):
                SEARCH_USERS_LIST[i] = None

    def __init__(self):
        super().__init__()

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(SCREEN_RESOLUTION[0] // 2 - MESSENGER_WINDOW_SIZE[0] // 2, SCREEN_RESOLUTION[1] // 2 - MESSENGER_WINDOW_SIZE[1] // 2, MESSENGER_WINDOW_SIZE[0], MESSENGER_WINDOW_SIZE[1])
        self.setStyleSheet('QWidget{\nbackground-color: rgb(16, 20, 25);}')

        self.auth_window_hint = WindowHint(self, HINT_HEIGHT, (26, 30, 35), 40)

        # Window hint
        self.auth_window_hint.setButton(lambda: self.close())
        self.auth_window_hint.setButtonText('🞩', ('Segoe UI', 21))
        self.auth_window_hint.setButtonStyles('QPushButton{\ncolor: white; background-color: rgb(26, 30, 35); border-radius: 0px;}QPushButton:hover{\nbackground-color: rgb(255, 30, 30);}')

        self.auth_window_hint.setButton(lambda: self.showMinimized())
        self.auth_window_hint.setButtonText('⎯', ('Segoe UI', 18))
        self.auth_window_hint.setButtonStyles('QPushButton{\ncolor: white; background-color: rgb(26, 30, 35); border-radius: 0px;}QPushButton:hover{\nbackground-color: rgb(56, 60, 65);}')

        # Search frame
        self.search_frame = QtWidgets.QFrame(self)
        self.search_frame.setGeometry(-1, HINT_HEIGHT, 401, 51)
        self.search_frame.setStyleSheet('QFrame{\nborder: 1px solid rgb(45, 50, 60);}')

        self.search_lineedit = QtWidgets.QLineEdit(self.search_frame)
        self.search_lineedit.setGeometry(10, 10, self.search_frame.width() - 60, 30)
        self.search_lineedit.setStyleSheet('QLineEdit{\nborder: 1px solid rgb(45, 50, 60); background-color: rgb(20, 24, 30); border-radius: 5px; color: white; pading: 5px;}')
        self.search_lineedit.setPlaceholderText("Поиск")

        self.search_button = QtWidgets.QPushButton(self.search_frame)
        self.search_button.setGeometry(self.search_frame.width() - 40, 10, 30, 30)
        self.search_button.setStyleSheet('QPushButton{\nbackground-image: url(images/magnifier.png); border: none;}')
        self.search_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_button.clicked.connect(self.search_for_users)

        # Messages frame
        self.messages_container = QtWidgets.QVBoxLayout()
        self.messages_container.addStretch(0)
        self.messages_frame = QtWidgets.QFrame(self)
        self.messages_frame.setGeometry(-1, HINT_HEIGHT + 50, 401, self.height() - HINT_HEIGHT - 49)
        self.messages_frame.setStyleSheet('QFrame{\nborder: 1px solid rgb(45, 50, 60);}')
        self.messages_frame.setLayout(self.messages_container)

        # Message title frame
        self.message_title_frame = QtWidgets.QLabel(self)
        self.message_title_frame.setGeometry(399, HINT_HEIGHT, self.width() - 398, 51)
        self.message_title_frame.setStyleSheet('QFrame{\nborder: 1px solid rgb(45, 50, 60); color: white;}')
        self.message_title_frame.setAlignment(QtCore.Qt.AlignCenter)
        self.message_title_frame.setFont(section_font)
        self.message_title_frame.setText(translate('', 'Выберите получателя...'))

        # Message frame
        self.message_frame = QtWidgets.QLabel(self)
        self.message_frame.setGeometry(399, HINT_HEIGHT + 50, self.width() + 1, self.height() - HINT_HEIGHT - 49)
        self.message_frame.setStyleSheet('QFrame{\nborder: 1px solid rgb(45, 50, 60); color: white;}')
        self.message_frame.setFont(lineedit_title_font)

        # Send frame
        self.send_frame = QtWidgets.QFrame(self)
        self.send_frame.setGeometry(399, self.height() - 50, self.width() - 395, 51)
        self.send_frame.setStyleSheet('QFrame{\nborder: 1px solid rgb(45, 50, 60);}')

        self.message_lineedit = QtWidgets.QLineEdit(self.send_frame)
        self.message_lineedit.setGeometry(10, 10, self.send_frame.width() - 60, 30)
        self.message_lineedit.setStyleSheet('QLineEdit{\nborder: 1px solid rgb(45, 50, 60); background-color: rgb(20, 24, 30); border-radius: 5px; color: white; pading: 5px;}')
        self.message_lineedit.setPlaceholderText("Ваше сообщение")

        self.send_button = QtWidgets.QPushButton(self.send_frame)
        self.send_button.setGeometry(self.send_frame.width() - 40, 10, 30, 30)
        self.send_button.setStyleSheet('QPushButton{\nbackground-image: url(images/plane.png); border: none;}')
        self.send_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.send_button.clicked.connect(lambda: send_message(username, getter, self.message_lineedit.text()))


class StartWindow(QtWidgets.QMainWindow):
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
    def show_registration_frame(self) -> None:

        self.registration_frame.hide()
        self.fade(self.registration_frame, 0)

        self.auth_frame.hide()
        self.registration_frame.show()
        self.unfade(self.registration_frame, 300)

    # Openg auth frame
    def show_auth_frame(self) -> None:

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
        self.auth_frame.setStyleSheet('QMainWindow{\nbackground-color: rgb(%s);}' % str(WINDOW_BACK_COLOR))

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
        self.login_button.clicked.connect(try_to_auth)

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

        self.registration_login_lineedit_label = QtWidgets.QLabel(self.registration_frame)
        self.registration_login_lineedit_label.setGeometry(self.registration_frame.width() // 6, 95, self.registration_frame.width() // 6 * 4, 20)
        self.registration_login_lineedit_label.setStyleSheet('QLabel{\ncolor: white;}')
        self.registration_login_lineedit_label.setText(translate('', 'Логин'))
        self.registration_login_lineedit_label.setFont(lineedit_title_font)

        self.registration_login_lineedit = QtWidgets.QLineEdit(self.registration_frame)
        self.registration_login_lineedit.setGeometry(self.registration_frame.width() // 6, 110, self.registration_frame.width() // 6 * 4, 40)
        self.registration_login_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); color: white; border: none; border-bottom: 2px solid white;}')
        self.registration_login_lineedit.setFont(lineedit_font)

        self.registration_password_lineedit = QtWidgets.QLabel(self.registration_frame)
        self.registration_password_lineedit.setGeometry(self.registration_frame.width() // 6, 185, self.registration_frame.width() // 6 * 4, 20)
        self.registration_password_lineedit.setStyleSheet('QLabel{\ncolor: white;}')
        self.registration_password_lineedit.setText(translate('', 'Пароль'))
        self.registration_password_lineedit.setFont(lineedit_title_font)

        self.registration_password_lineedit = QtWidgets.QLineEdit(self.registration_frame)
        self.registration_password_lineedit.setGeometry(self.registration_frame.width() // 6, 200, self.registration_frame.width() // 6 * 4, 40)
        self.registration_password_lineedit.setStyleSheet('QLineEdit{\nbackground-color: rgba(0, 0, 0, 0); color: white; border: none; border-bottom: 2px solid white;}')
        self.registration_password_lineedit.setFont(lineedit_font)

        self.registation_registration_button = QtWidgets.QPushButton(self.registration_frame)
        self.registation_registration_button.setGeometry(self.registration_frame.width() // 6, 255, self.registration_frame.width() // 6 * 2 - 5, 40)
        self.registation_registration_button.setStyleSheet('QPushButton{\nborder-radius: 6px; background-color: rgb(6, 17, 185); color: white;}')
        self.registation_registration_button.setText(translate('', 'Регистрация'))
        self.registation_registration_button.setFont(lineedit_title_font)
        self.registation_registration_button.clicked.connect(try_to_registrate)

        self.registation_login_button = QtWidgets.QPushButton(self.registration_frame)
        self.registation_login_button.setGeometry(self.registration_frame.width() // 6 * 3 + 5, 255, self.registration_frame.width() // 6 * 2 - 5, 40)
        self.registation_login_button.setStyleSheet('QPushButton{\nborder-radius: 6px; background-color: rgb(5, 5, 5); border: 1px solid rgb(6, 17, 185); color: rgb(6, 17, 185);}')
        self.registation_login_button.setText(translate('', 'Автоизация'))
        self.registation_login_button.setFont(lineedit_title_font)
        self.registation_login_button.clicked.connect(self.show_auth_frame)

        self.registration_frame.hide()


# Server
def start_server():
    global server
    global username
    global password

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('178.250.158.150', 7070))

    while True:
        global SEARCH_USERS_LIST
        global MESSAGE_USERS_LIST
        server_data = server.recv(4096).decode('utf-8')
        if server_data:
            print('[SERVER]:', server_data)

            if server_data == 'useralreadyexist':
                ctypes.windll.user32.MessageBoxW(0, 'Пользователь с данным логином уже существует.', 'Ошибка', 0x10)

            if server_data == 'usernotexist':
                ctypes.windll.user32.MessageBoxW(0, 'Пользователя с данным логином не существует.', 'Ошибка', 0x10)

            if server_data == 'wrongpassword':
                ctypes.windll.user32.MessageBoxW(0, 'Неверный пароль.', 'Ошибка', 0x10)

            if server_data.startswith('auth') or server_data.startswith('authsuccess'):
                username, password = server_data.split(' ')[1], server_data.split(' ')[2]
                messanger_window.close()
                threading.Thread(target=show_main_window).start()

            if server_data.startswith('userslist'):
                users = ast.literal_eval(server_data.split(' ')[1])
                for index, user in enumerate(users):
                    user = user.split('.txt')[0]
                    SEARCH_USERS_LIST[index] = user.encode()

            if server_data.startswith('message'):
                message_data = server_data.split(' ', 2)
                data = ast.literal_eval(message_data[1])
                message = ast.literal_eval(message_data[2])
                if data[1] == username:
                    window.message_frame.setText(translate('', f'{window.message_frame.text()}{data[0]} -> {data[1]} : {decode_chars(message)}\n'))
                if data[0] == username:
                    window.message_frame.setText(translate('', f'{window.message_frame.text()}{data[0]} -> {data[1]} : {decode_chars(message)}\n'))

            if server_data == 'stop':
                break


def show_main_window():
    global window
    application = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    application.exec()


application = QtWidgets.QApplication(sys.argv)
messanger_window = StartWindow()
threading.Thread(target=start_server).start()
messanger_window.show()
application.exec()
# show_main_window()
