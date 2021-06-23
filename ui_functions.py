import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt, QVariantAnimation, QAbstractAnimation
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont, QColor


class MyBar(QWidget):

    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = QLabel("")
        font = QFont()
        font.setPointSize(15)
        font.setFamily("Sitka")
        self.title.setFont(font)

        btn_size = 13

        self.btn_close = QPushButton()
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)
        self.btn_close.setContentsMargins(10, 10, 10, 10)
        self.btn_close.setStyleSheet("QPushButton {\n"
            "    border-radius: 8px;\n"
            "    background-image: url(images/close.png);\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    color: rgb(255, 255, 255);\n"
            "    background-image: url(images/close_hover.png);\n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
        "")

        self.btn_min = QPushButton()
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet("QPushButton {\n"
            "    border-radius: 8px;\n"
            "    background-image: url(images/minimize.png);\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    color: rgb(255, 255, 255);\n"
            "    background-image: url(images/minimize_hover.png);\n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
        "")

        self.title.setFixedHeight(30)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("""
            background-color: black;
            color: white;
        """)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()

    def btn_min_clicked(self):
        self.parent.showMinimized()

class PushButtonEffect(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation = QVariantAnimation(
            startValue=QColor("#363636"),
            endValue=QColor("#0f1923"),
            valueChanged=self._on_value_changed,
            duration=400,
        )
        self._update_stylesheet(QColor("white"), QColor("white"))

    def _on_value_changed(self, color):
        foreground = (
            QColor("#FF8C00")
            if self._animation.direction() == QAbstractAnimation.Forward
            else QColor("#FF8C00")
        )
        self._update_stylesheet(color, foreground)
    
    def _update_stylesheet(self, background, foreground):

        self.setStyleSheet(
            "QPushButton {\n" +
            "background-image: url();\n" +
            f"background-color: {background.name()};\n" +
            "padding: 8px;\n" +
            "font-size: 0.8rem;\n" +
            "font-weight: 900;\n" +
            f"color: {foreground.name()};\n" +
            "text-align: center;\n" +
            "text-transform: uppercase;\n" +
            "text-decoration: none;\n" +
            "position: relative;\n" +
            "border: 1px solid;\n" +
            f"border-color: {foreground.name()};\n" +
            "border-radius: 8px;\n" +
            "max-width: 240px;\n" +
            "padding: 8px;\n" +
            "width: 100%;\n" +
            "}"
        )
    
    def enterEvent(self, event):
        self._animation.setDirection(QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self._animation.setDirection(QAbstractAnimation.Forward)
        self._animation.start()
        super().leaveEvent(event)

