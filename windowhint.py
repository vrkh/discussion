from PyQt5 import QtWidgets, QtCore, QtGui


class WindowHint:

    def mousePressEvent(self, evt) -> None:
        self.first_pos = (evt.globalPos().x(), evt.globalPos().y())

    def mouseMoveEvent(self, evt):
        try:
            delta = (evt.globalPos().x() - self.first_pos[0], evt.globalPos().y() - self.first_pos[1])
            self.__parent.move(self.__parent.x() + delta[0], self.__parent.y() + delta[1])
            self.first_pos = (evt.globalPos().x(), evt.globalPos().y())
        except Exception:
            pass

    def __init__(self, parent: object, height: int, color: tuple, buttons_width: int) -> None:

        self.__height = height
        self.__parent = parent
        self.__buttons_width = buttons_width
        self.__buttons_amounth = 0
        self._translate = QtCore.QCoreApplication.translate

        self.hint_frame = QtWidgets.QFrame(parent)
        self.hint_frame.setGeometry(0, 0, parent.width(), height)
        self.hint_frame.setStyleSheet("QFrame{\nbackground-color: rgb(%s, %s, %s)}" % (str(color[0]), str(color[1]), str(color[2])))
        self.hint_frame.mousePressEvent = self.mousePressEvent
        self.hint_frame.mouseMoveEvent = self.mouseMoveEvent

    # Buttons
    def setButton(self, function) -> None:
        self.button = QtWidgets.QPushButton(self.hint_frame)
        self.button.setGeometry(self.__parent.width() - self.__buttons_width - self.__buttons_amounth * self.__buttons_width, 0, self.__buttons_width, self.__height)
        self.button.clicked.connect(lambda: function())
        self.button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.__buttons_amounth += 1

    def setButtonText(self, text: str, font: tuple) -> None:
        self.font = QtGui.QFont()
        self.font.setFamily(font[0])
        self.font.setPointSize(font[1])
        self.button.setFont(self.font)
        self.button.setText(self._translate("close", text))

    def setButtonStyles(self, style: str) -> None:
        self.button.setStyleSheet(style)
