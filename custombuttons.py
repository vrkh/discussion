from PyQt5 import QtWidgets, QtCore, QtGui


class MenuButton(QtWidgets.QPushButton):

    def return_first_styles(self):
        self.setStyleSheet("QPushButton{\nbackground-color: %s; border-radius: 0px; text-align: left; color: %s; background-image: url(%s)}" % (self.start_color, self.start_text_color, self.image))

    def _on_value_changed(self, color):
        foreground = (QtGui.QColor(f"{self.start_text_color}") if self._animation.direction() == QtCore.QAbstractAnimation.Forward else QtGui.QColor(f"{self.stop_text_color}"))
        self._update_stylesheet(color, foreground)

    def _update_stylesheet(self, background, foreground):

        if not self.status:
            self.setStyleSheet(
                """
            QPushButton{
                background-color: %s;
                color: %s;
                background-image: url(%s);
                background-position: center;
                border-radius: 0px;
                text-align: left;
            }
            """
                % (background.name(), foreground.name(), str(self.image)))
        else:
            self.setStyleSheet(
                """
            QPushButton{
                background-color: %s;
                color: %s;
                background-image: url(%s);
                background-position: center;
                border-radius: 0px;
                text-align: left;
            }
            """
                % (self.stop_color, foreground.name(), str(self.image)))

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().leaveEvent(event)

    def __init__(self, parent, x: int, y: int, width: int, height: int, start_color: int, stop_color: int, start_text_color: str, stop_text_color: str, duration: int, status, image=None) -> None:
        super().__init__(parent)

        self.image = image
        self.start_color = start_color
        self.stop_color = stop_color
        self.start_text_color = start_text_color
        self.stop_text_color = stop_text_color
        self.duration = duration
        self.status = status
        self.setGeometry(x, y, width, height)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.enable_frame = QtWidgets.QFrame(self)
        self.enable_frame.setGeometry(0, 0, 3, height)
        self.enable_frame.setStyleSheet("QFrame{\nbackground-color: %s;}" % stop_text_color)

        self._translate = QtCore.QCoreApplication.translate
        self._animation = QtCore.QVariantAnimation(startValue=QtGui.QColor(stop_color), endValue=QtGui.QColor(start_color), valueChanged=self._on_value_changed, duration=duration)
        self._update_stylesheet(QtGui.QColor(f"{self.start_text_color}"), QtGui.QColor(f"{self.stop_text_color}"))
        if not self.status:
            self.enable_frame.hide()
            self.setStyleSheet("QPushButton{\nbackground-color: %s; border-radius: 0px; text-align: left; color: %s; background-image: url(%s)}" % (self.start_color, self.start_text_color, self.image))
        else:
            self.setStyleSheet("QPushButton{\nbackground-color: %s; border-radius: 0px; text-align: left; color: %s; background-image: url(%s)}" % (self.stop_color, self.stop_text_color, self.image))


class MainButton(QtWidgets.QPushButton):

    def _on_value_changed(self, color):
        foreground = (QtGui.QColor(f"{self.start_text_color}") if self._animation.direction() == QtCore.QAbstractAnimation.Forward else QtGui.QColor(f"{self.stop_text_color}"))
        self._update_stylesheet(color, foreground)

    def _update_stylesheet(self, background, foreground):

        self.setStyleSheet(
            """
        QPushButton{
            background-color: %s;
            color: %s;
            background-position: center;
            border-radius: 6px;
        }
        """
            % (background.name(), foreground.name()))

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().leaveEvent(event)

    def __init__(self, parent: object, x: int, y: int, width: int, height: int, start_color: int, stop_color: int, start_text_color: str, stop_text_color: str, duration: int):
        super().__init__(parent)

        self.start_color = start_color
        self.stop_color = stop_color
        self.start_text_color = start_text_color
        self.stop_text_color = stop_text_color
        self.duration = duration
        self.setGeometry(x, y, width, height)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self._translate = QtCore.QCoreApplication.translate
        self._animation = QtCore.QVariantAnimation(startValue=QtGui.QColor(stop_color), endValue=QtGui.QColor(start_color), valueChanged=self._on_value_changed, duration=duration)
        self._update_stylesheet(QtGui.QColor(f"{self.start_text_color}"), QtGui.QColor(f"{self.stop_text_color}"))
        self.setStyleSheet("QPushButton{\nbackground-color: %s; border-radius: 6px; color: %s;}" % (self.start_color, self.start_text_color))
