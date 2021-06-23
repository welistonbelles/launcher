import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QScrollBar, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QFrame, QProgressBar, QListWidget, QTextBrowser, QScrollArea
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QFont, QColor, QPixmap
from PyQt5.QtCore import Qt, QVariantAnimation, QAbstractAnimation

# Import ui_functions
from ui_functions import MyBar, PushButtonEffect
from launcher_functions import *

# GLOBAL_VARIABLE
GLOBAL_SLIDE = 1

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Bleach Launcher")
        self.setFixedSize(799, 569)
        self.setStyleSheet(
            'background-image: url("images/title_bar.png"); border-radius: 5px; background-color: transparent; '
        )
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.contentFrame = QFrame(self)
        self.contentFrame.setFrameShape(QFrame.StyledPanel)
        self.contentFrame.setFrameShadow(QFrame.Raised)
        self.contentFrame.setObjectName("contentFrame")
        self.contentFrame.setContentsMargins(0, 0, 0, 0)
        self.contentFrame.setFixedSize(800, 570)
        self.contentFrame.setGeometry(QtCore.QRect(0, 0, 800, 570))
        self.contentFrame.setStyleSheet('border-radius: 5px; background-color: transparent; ')

        # Cria a title bar
        self.layout  = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addStretch(-1)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.pressing = False

        # Cria um frame para o icon
        self.frameIcon = QFrame(self)
        self.frameIcon.setFrameShape(QFrame.StyledPanel)
        self.frameIcon.setFrameShadow(QFrame.Raised)
        self.frameIcon.setObjectName("frameIcon")
        self.frameIcon.setContentsMargins(0, 0, 0, 0)
        self.frameIcon.setFixedSize(32, 32)
        self.frameIcon.setStyleSheet('background-image: url("images/icon.png");')

        # Cria um novo frame para o conteudo abaixo da title bar
        self.contentFrame = QFrame(self)
        self.contentFrame.setFrameShape(QFrame.StyledPanel)
        self.contentFrame.setFrameShadow(QFrame.Raised)
        self.contentFrame.setObjectName("contentFrame")
        self.contentFrame.setContentsMargins(0, 0, 0, 0)
        self.contentFrame.setFixedSize(800, 540)
        self.contentFrame.setGeometry(QtCore.QRect(-1, 30, 801, 540))
        self.contentFrame.setStyleSheet('background-color: transparent; background-image: url("images/background.png"); background-position: center; border-radius: 5px;')


        # Cria a progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(46, 510, 583, 23))
        self.progressBar.setStyleSheet("QProgressBar {\n"
        "    background-color: rgb(134, 73, 0);\n"
        "    color: rgb(0, 255, 0);\n"
        "    border-style: solid;\n"
        "    border-radius: 10px;\n"
        "    text-align: center;\n"
        "    background-image: url()}\n"
        "\n"
        "QProgressBar::chunk {\n"
        "    border-radius: 10px;\n"
        "    background-image: url();\n"
        "    background-color: qlineargradient(spread:pad, x1:0.123, y1:0.193182, x2:1, y2:0, stop:0.360063 rgba(255, 85, 0, 249), stop:1 rgba(255, 255, 255, 255));\n"
        "}")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")


        # Cria um novo frame para o rodape
        self.baseboard = QFrame(self)
        self.baseboard.setFrameShape(QFrame.StyledPanel)
        self.baseboard.setFrameShadow(QFrame.Raised)
        self.baseboard.setObjectName("baseboard")
        self.baseboard.setContentsMargins(0, 0, 0, 0)
        self.baseboard.setFixedSize(794, 89)
        self.baseboard.setGeometry(QtCore.QRect(2, 478, 794, 89))
        self.baseboard.setStyleSheet("QFrame {\n"
        "background-image: url(images/baseboard);\n"
        "background-position: center;\n"
        "border-radius: 12px;\n"
        "}\n"
        )

        # Cria um label para o texto de status
        self.labelStats = QLabel(self.baseboard)
        self.labelStats.setGeometry(QtCore.QRect(250, 62, 180, 20))
        self.labelStats.setStyleSheet("QLabel {\n"
        "    background-image: url();\n"
        "    \n"
        "    \n"
        "    color: rgb(222, 222, 222);\n"
        "}")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setFamily("Sitka")
        self.labelStats.setFont(font)
        self.labelStats.setObjectName("labelStats")
        self.labelStats.setAlignment(QtCore.Qt.AlignCenter)
        #self.labelStats.setText()

        # Cria um label para o texto informando quantia de arquivos
        self.labelCount = QLabel(self.baseboard)
        self.labelCount.setGeometry(QtCore.QRect(130, 10, 145, 16))
        self.labelCount.setStyleSheet("QLabel {\n"
        "    background-image: url();\n"
        "    \n"
        "    \n"
        "    color: rgb(222, 222, 222);\n"
        "}")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setFamily("Fixedsys")
        self.labelCount.setFont(font)
        self.labelCount.setObjectName("labelCount")

        # Cria um label para o texto informando a velocidade de download
        self.labelRate = QLabel(self.baseboard)
        self.labelRate.setGeometry(QtCore.QRect(330, 10, 145, 16))
        self.labelRate.setStyleSheet("QLabel {\n"
        "    background-image: url();\n"
        "    \n"
        "    \n"
        "    color: rgb(222, 222, 222);\n"
        "}")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setFamily("Fixedsys")
        self.labelRate.setFont(font)
        self.labelRate.setObjectName("labelRate")

        # Cria um label para o texto informando o tamanho do download
        self.labelSize = QLabel(self.baseboard)
        self.labelSize.setGeometry(QtCore.QRect(470, 10, 145, 16))
        self.labelSize.setStyleSheet("QLabel {\n"
        "    background-image: url();\n"
        "    \n"
        "    text-align: center;\n"
        "    color: rgb(255, 255, 255);\n"
        "}")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setFamily("Fixedsys")
        self.labelSize.setFont(font)
        self.labelSize.setObjectName("labelSize")

        # Cria o botao de jogar
        self.button_play = QPushButton(self.baseboard)
        self.button_play.setEnabled(False)
        self.button_play.setGeometry(QtCore.QRect(650, 8, 126, 66))
        self.button_play.setMinimumSize(QtCore.QSize(126, 66))
        self.button_play.setMaximumSize(QtCore.QSize(126, 66))
        self.button_play.setStyleSheet("QPushButton {\n"
        "    border-radius: 8px;\n"
        "    background-image: url(images/play.png);\n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "    color: rgb(255, 255, 255);\n"
        "    background-image: url(images/play_hover.png);\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    color: rgb(255, 255, 255);\n"
        "}\n"
        "")
        self.button_play.setText("")
        self.button_play.setObjectName("button_play")
        self.button_play.clicked.connect(lambda: playClicked(self))

        # scroll bar
        scroll_bar = QScrollBar(self.contentFrame)
        scroll_bar.setStyleSheet("""
            QScrollBar::vertical {
                background-image: url();
                background-color: rgb(248, 171, 54);
                border: none;
                width: 14px;
                border-radius: 0px
            }
            QScrollBar::handle::vertical {
                background-image: url();
                background-color: rgb(255, 149, 19);
                border-radius: 7px;
                min-height: 30px;
            }
            QScrollBar::handle::vertical:hover {
                background-color: rgb(255, 85, 0);
            }
            QScrollBar::handle::vertical:pressed {
                background-color: rgb(255, 177, 82);
            }
        
        """)

        # Cria a lista de atts recentes 
        self.listWidget = QListWidget(self.contentFrame)
        self.listWidget.setGeometry(QtCore.QRect(29, 292, 498, 85))
        self.listWidget.setObjectName("listWidget")
        #self.listWidget.itemClicked.connect(self.showInformationInLabelAtt)
        self.listWidget.itemSelectionChanged.connect(self.showInformationInLabelAtt)
        self.listWidget.setVerticalScrollBar(scroll_bar)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setFamily("Arial Black")
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("QListWidget {\n"
        "    background-image: url();\n"
        "    background-color: transparent;\n"
        "    color: white;\n"
        "}\n"
        "QListView::item:selected {\n"
        "   background-color: rgb(250, 176, 110);\n"
        "   color: rgb(74, 74, 74);\n"
        "   border : 0px solid black;\n"
        "}\n"
        "")

         # scroll bar
        scrollAtts = QScrollBar(self.contentFrame)
        scrollAtts.setStyleSheet("""
            QScrollBar::vertical {
                background-image: url();
                background-color: rgb(248, 171, 54);
                border: none;
                width: 14px;
                border-radius: 0px
            }
            QScrollBar::handle::vertical {
                background-image: url();
                background-color: rgb(255, 149, 19);
                border-radius: 7px;
                min-height: 30px;
            }
            QScrollBar::handle::vertical:hover {
                background-color: rgb(255, 85, 0);
            }
            QScrollBar::handle::vertical:pressed {
                background-color: rgb(255, 177, 82);
            }
        
        """)

        # Cria uma Scroll Area
        self.scrollLabel = QScrollArea(self.contentFrame)
        self.scrollLabel.setGeometry(QtCore.QRect(31, 14, 496, 267))
        self.scrollLabel.setWidgetResizable(True)
        self.scrollLabel.setObjectName("scrollLabel")
        self.scrollLabel.setVerticalScrollBar(scrollAtts)
        self.scrollLabel.setStyleSheet("""
            QScrollArea {
                background-image: url();
            }
        """)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 482, 267))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setStyleSheet("background-image: url(); background-color: transparent; color: white;")

        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        # Cria um label para apresentar o titulo das atts
        self.labelTittleAtts = QLabel(self.scrollAreaWidgetContents)
        self.labelTittleAtts.setStyleSheet("background-color: transparent;")
        self.labelTittleAtts.setMinimumSize(QtCore.QSize(0, 30))
        self.labelTittleAtts.setObjectName("labelTittleAtts")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setFamily("Arial Black")
        self.labelTittleAtts.setFont(font)
        self.verticalLayout.addWidget(self.labelTittleAtts)
        # Cria um label para apresentar o conteudo das atts
        self.labelAtts = QLabel(self.scrollAreaWidgetContents)
        self.labelAtts.setGeometry(QtCore.QRect(0, 0, 496, 267))
        self.labelAtts.setMinimumSize(QtCore.QSize(0, 500))
        self.labelAtts.setStyleSheet("QLabel {\n"
        "    background-image: url();\n"
        "    background-color: transparent;\n"
        "    border-radius: 0px;\n"
        "    color: rgb(255, 255, 255);\n"
        "    text-align: center;\n"
        "}")
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setFamily("Arial Black")
        self.labelAtts.setFont(font)
        self.labelAtts.setObjectName("labelAtts")
        #self.labelAtts.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAtts.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.labelAtts)
        self.scrollLabel.setWidget(self.scrollAreaWidgetContents)



        # Cria o botao de slide
        self.slide1 = QPushButton(self.contentFrame)
        self.slide1.setEnabled(True)
        self.slide1.setGeometry(QtCore.QRect(595, 372, 26, 27))
        self.slide1.setMinimumSize(QtCore.QSize(26, 27))
        self.slide1.setMaximumSize(QtCore.QSize(26, 27))
        self.slide1.setStyleSheet("QPushButton {\n"
        "    border-radius: 4px;\n"
        "    background-image: url(images/button_pressed.png);\n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "    color: rgb(255, 255, 255);\n"
        "    background-image: url(images/button_hover.png);\n"
        "    border-radius: 4px; }\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-image: url(images/button_pressed.png);\n"
        "}\n"
        "")
        self.slide1.setText("")
        self.slide1.setObjectName("slide1")
        self.slide1.clicked.connect(lambda: setImageSlideBar(self, 1))

        global GLOBAL_OLDBUTTON
        GLOBAL_OLDBUTTON = self.slide1

        # Cria o botao2 de slide
        self.slide2 = QPushButton(self.contentFrame)
        self.slide2.setEnabled(True)
        self.slide2.setGeometry(QtCore.QRect(630, 372, 26, 27))
        self.slide2.setMinimumSize(QtCore.QSize(26, 27))
        self.slide2.setMaximumSize(QtCore.QSize(26, 27))
        self.slide2.setStyleSheet("QPushButton {\n"
        "    border-radius: 4px;\n"
        "    background-image: url(images/button_normal.png);\n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "    color: rgb(255, 255, 255);\n"
        "    background-image: url(images/button_hover.png);\n"
        "    border-radius: 4px}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-image: url(images/button_pressed.png);}\n"
        "")
        self.slide2.setText("")
        self.slide2.setObjectName("slide2")
        self.slide2.clicked.connect(lambda: setImageSlideBar(self, 2))

        # Cria o botao3 de slide
        self.slide3 = QPushButton(self.contentFrame)
        self.slide3.setEnabled(True)
        self.slide3.setGeometry(QtCore.QRect(665, 372, 26, 27))
        self.slide3.setMinimumSize(QtCore.QSize(26, 27))
        self.slide3.setMaximumSize(QtCore.QSize(26, 27))
        self.slide3.setStyleSheet("QPushButton {\n"
        "    border-radius: 4px;\n"
        "    background-image: url(images/button_normal.png);\n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "    color: rgb(255, 255, 255);\n"
        "    background-image: url(images/button_hover.png);\n"
        "    border-radius: 4px}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-image: url(images/button_pressed.png);\n"
        "    }\n"
        "")
        self.slide3.setText("")
        self.slide3.setObjectName("slide3")
        self.slide3.clicked.connect(lambda: setImageSlideBar(self, 3))

        # Cria o botao4 de slide
        self.slide4 = QPushButton(self.contentFrame)
        self.slide4.setEnabled(True)
        self.slide4.setGeometry(QtCore.QRect(700, 372, 26, 27))
        self.slide4.setMinimumSize(QtCore.QSize(26, 27))
        self.slide4.setMaximumSize(QtCore.QSize(26, 27))
        self.slide4.setStyleSheet("QPushButton {\n"
        "    border-radius: 4px;\n"
        "    background-image: url(images/button_normal.png);\n"
        "}\n"
        "QPushButton:hover {\n"
        "    color: rgb(255, 255, 255);\n"
        "    background-image: url(images/button_hover.png);\n"
        "    border-radius: 4px};\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-image: url(images/button_pressed.png);\n"
        "}\n"
        "")
        self.slide4.setText("")
        self.slide4.setObjectName("slide4")
        self.slide4.clicked.connect(lambda: setImageSlideBar(self, 4))

        # Cria o botao5 de slide
        self.slide5 = QPushButton(self.contentFrame)
        self.slide5.setEnabled(True)
        self.slide5.setGeometry(QtCore.QRect(735, 372, 26, 27))
        self.slide5.setMinimumSize(QtCore.QSize(26, 27))
        self.slide5.setMaximumSize(QtCore.QSize(26, 27))
        self.slide5.setStyleSheet("QPushButton {\n"
        "    border-radius: 4px;\n"
        "    background-image: url(images/button_normal.png);\n"
        "}\n"
        "QPushButton:hover {\n"
        "    color: rgb(255, 255, 255);\n"
        "    background-image: url(images/button_hover.png);\n"
        "    border-radius: 4px;}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-image: url(images/button_pressed.png);\n"
        "}\n"
        "")
        self.slide5.setText("")
        self.slide5.setObjectName("slide5")
        self.slide5.clicked.connect(lambda: setImageSlideBar(self, 5))

        # Cria um novo frame para o conteudo abaixo da title bar
        self.slideFrame = QTextBrowser(self)
        #self.slideFrame.setFrameShape(QFrame.StyledPanel)
        #self.slideFrame.setFrameShadow(QFrame.Raised)
        self.slideFrame.setObjectName("slideFrame")
        self.slideFrame.setContentsMargins(0, 0, 0, 0)
        self.slideFrame.setFixedSize(200, 280)
        self.slideFrame.setGeometry(QtCore.QRect(571, 119, 200, 280))
        self.slideFrame.setStyleSheet(
            'background-image: url("images/1.png");'  + 
            'background-position: center;' +
            'border-radius: 0px;'
        )

        # Cria um novo frame para armazenar o botao de Learn To Play
        self.btnFrame = QFrame(self)
        self.btnFrame.setObjectName("btnFrame")
        self.btnFrame.setContentsMargins(0, 0, 0, 0)
        self.btnFrame.setFixedSize(215, 34)
        self.btnFrame.setGeometry(QtCore.QRect(565, 35, 212, 75))
        self.btnFrame.setStyleSheet(
            'background-image: url();'  + 
            'background-position: center;' +
            'border-radius: 0px;'
        )

        # Cria o botao de aprenda a jogar
        self.btnLearnToPlay = PushButtonEffect()
        self.btnLearnToPlay.setEnabled(True)
        self.btnLearnToPlay.setGeometry(QtCore.QRect(500, 2, 215, 34))
        self.btnLearnToPlay.setMinimumSize(QtCore.QSize(215, 34))
        self.btnLearnToPlay.setStyleSheet("""
            QPushButton {
                background-image: url();
                background-color: #0f1923;
                width: 100%;
                max-width: 240px;
                padding: 8px;
                font-size: 0.8rem;
                font-weight: 900;
                color: rgb(245, 117, 11);
                text-align: center;
                text-transform: uppercase;
                text-decoration: none;
                position: relative;
                border: 1px solid;
                border-color: rgb(245, 117, 11);
                border-radius: 8px;
            }
            QPushButton:hover {
                color: #ece8e1;
                background-color: rgb(245, 117, 11);
            }
        
        """)
        
        self.btnLearnToPlay.setText("Aprenda a Jogar")
        self.btnLearnToPlay.setObjectName("btnLearnToPlay")
        self.btnLearnToPlay.clicked.connect(lambda: learnToPlay(self))
        font = QFont()
        font.setPointSize(11)
        font.setFamily("Muli")
        self.btnLearnToPlay.setFont(font)
        self.btnLayout  = QVBoxLayout(self.btnFrame)
        self.btnLayout.setContentsMargins(0,0,0,0)
        self.btnLayout.addWidget(self.btnLearnToPlay)
        self.btnLayout.setGeometry(QtCore.QRect(500, 2, 215, 34))

        # Cria um novo frame para armazenar o botao de Criar Conta
        self.btnFrame2 = QFrame(self)
        self.btnFrame2.setObjectName("btnFrame2")
        self.btnFrame2.setContentsMargins(0, 0, 0, 0)
        self.btnFrame2.setFixedSize(215, 34)
        self.btnFrame2.setGeometry(QtCore.QRect(565, 73, 212, 75))
        self.btnFrame2.setStyleSheet(
            'background-image: url();'  + 
            'background-position: center;' +
            'border-radius: 0px;'
        )

        # Cria o botao de criar conta
        self.btnCreateAccount = PushButtonEffect()
        self.btnCreateAccount.setEnabled(True)
        self.btnCreateAccount.setGeometry(QtCore.QRect(660, 46, 120, 24))
        self.btnCreateAccount.setMinimumSize(QtCore.QSize(215, 34))
        self.btnCreateAccount.setStyleSheet("""
            QPushButton {
                background-image: url();
                background-color: #0f1923;
                width: 100%;
                max-width: 240px;
                padding: 8px;
                font-size: 0.8rem;
                font-weight: 900;
                color: rgb(245, 117, 11);
                text-align: center;
                text-transform: uppercase;
                text-decoration: none;
                position: relative;
                border: 1px solid;
                border-color: rgb(245, 117, 11);
                border-radius: 8px;
            }
            QPushButton:hover {
                color: #ece8e1;
                background-color: rgb(245, 117, 11);
            }
        
        """)
        self.btnCreateAccount.setText("Criar Conta")
        self.btnCreateAccount.setObjectName("btnCreateAccount")
        self.btnCreateAccount.clicked.connect(lambda: createAccount(self))
        font = QFont()
        font.setPointSize(11)
        font.setFamily("Muli")
        self.btnCreateAccount.setFont(font)

        self.btnLayout2  = QVBoxLayout(self.btnFrame2)
        self.btnLayout2.setContentsMargins(0,0,0,0)
        self.btnLayout2.addWidget(self.btnCreateAccount)
        self.btnLayout2.setGeometry(QtCore.QRect(500, 2, 215, 34))


        # Cria frame para logo
        self.frameLogo = QFrame(self.contentFrame)
        self.frameLogo.setGeometry(QtCore.QRect(220, 330, 302, 115))
        self.frameLogo.setStyleSheet("QFrame {\n"
        "    background-image: url(images/logo.png);\n"
        "    background-color: transparent;\n"
        "}")
        self.frameLogo.setObjectName("frameLogo")





        def playClicked(self):
            openGame(self)
        
        def learnToPlay(self):
            site = "https://permita.me/?q=ainda+n%C3%A3o+possuimos+site+amigo"
            os.system(f"start \"\" {site}") # Por enquanto esta redirecionando pro google

        def createAccount(self):
            site = "https://permita.me/?q=ainda+n%C3%A3o+possuimos+site+amigo"
            os.system(f"start \"\" {site}") # Por enquanto esta redirecionando pro google

        def setImageSlideBar(self, id):
            global GLOBAL_SLIDE

            if id > 5:
                id = 1
            elif id < 1:
                id = 5
                
            self.slideFrame.setStyleSheet(
                f'background-image: url("images/{id}.png");'  + 
                'background-position: center;' +
                'border-radius: 0px;'
            )

            oldBtn = self.findChild(QPushButton, f"slide{GLOBAL_SLIDE}")
            oldBtn.setStyleSheet("QPushButton {\n"
            "    border-radius: 4px;\n"
            f"    background-image: url(images/button_normal.png);\n"
            "}\n"
            "QPushButton:hover {\n"
            "    color: rgb(255, 255, 255);\n"
            f"    background-image: url(images/button_hover.png);\n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            f"    background-image: url(images/button_pressed.png);\n"
            "}\n"
            "")
            newBtn = self.findChild(QPushButton, f"slide{id}")
            newBtn.setStyleSheet("QPushButton {\n"
            "    border-radius: 4px;\n"
            f"    background-image: url(images/button_pressed.png);\n"
            "}\n"
            "QPushButton:hover {\n"
            "    color: rgb(255, 255, 255);\n"
            f"    background-image: url(images/button_hover.png);\n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            f"    background-image: url(images/button_pressed.png);\n"
            "}\n"
            "")
            GLOBAL_SLIDE = id


    def showInformationInLabelAtt(self):
        attInformationInLabelAtt(self, self.listWidget.currentItem().text())

    def Testando(self):
        checkNotices(window)
        client = checkBaseDirectory(window)
        if client:
            if checkCurrentVersion(window):
                self.button_play.setEnabled(True)
            #checkAttArchives(window)
        self.labelStats.setText("Client Atualizado.")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    QtCore.QTimer.singleShot(1, window.Testando)
    
    sys.exit(app.exec_())