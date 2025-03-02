# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI_FloatWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QProgressBar, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_FloatWindow(object):
    def setupUi(self, FloatWindow):
        if not FloatWindow.objectName():
            FloatWindow.setObjectName(u"FloatWindow")
        FloatWindow.resize(960, 150)
        FloatWindow.setMinimumSize(QSize(960, 150))
        FloatWindow.setMaximumSize(QSize(3840, 2160))
        self.verticalLayout = QVBoxLayout(FloatWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(FloatWindow)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u".QWidget {background-color: rgba(0, 0, 0, 160);\n"
"color: rgba(255, 255, 255, 220);}")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.TextLabel = QLabel(self.widget)
        self.TextLabel.setObjectName(u"TextLabel")
        font = QFont()
        font.setPointSize(64)
        font.setBold(True)
        self.TextLabel.setFont(font)
        self.TextLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.TextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.TextLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.TextLabel)

        self.RestTimeProgressBar = QProgressBar(self.widget)
        self.RestTimeProgressBar.setObjectName(u"RestTimeProgressBar")
        self.RestTimeProgressBar.setMaximumSize(QSize(16777215, 10))
        self.RestTimeProgressBar.setStyleSheet(u"QProgressBar {background-color: rgba(0, 0, 0, 0);}\n"
"QProgressBar::chunk {background-color: rgb(55, 205, 84)}")
        self.RestTimeProgressBar.setMaximum(100000)
        self.RestTimeProgressBar.setValue(100000)
        self.RestTimeProgressBar.setTextVisible(False)
        self.RestTimeProgressBar.setTextDirection(QProgressBar.Direction.TopToBottom)

        self.verticalLayout_2.addWidget(self.RestTimeProgressBar)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(FloatWindow)

        QMetaObject.connectSlotsByName(FloatWindow)
    # setupUi

    def retranslateUi(self, FloatWindow):
        FloatWindow.setWindowTitle(QCoreApplication.translate("FloatWindow", u"CallYouMsgWindow", None))
        self.TextLabel.setText(QCoreApplication.translate("FloatWindow", u"MsgContent", None))
    # retranslateUi

