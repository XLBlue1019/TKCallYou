# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI_Send.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Send(object):
    def setupUi(self, Send):
        if not Send.objectName():
            Send.setObjectName(u"Send")
        Send.resize(449, 311)
        self.verticalLayout_2 = QVBoxLayout(Send)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(Send)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.titleLabel = QLabel(self.widget)
        self.titleLabel.setObjectName(u"titleLabel")
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.titleLabel.setFont(font)

        self.horizontalLayout_3.addWidget(self.titleLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.aboutPbtn = QPushButton(self.widget)
        self.aboutPbtn.setObjectName(u"aboutPbtn")

        self.horizontalLayout_3.addWidget(self.aboutPbtn)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.label_2.setFont(font1)

        self.verticalLayout.addWidget(self.label_2)

        self.MessageEdit = QLineEdit(self.widget)
        self.MessageEdit.setObjectName(u"MessageEdit")
        font2 = QFont()
        font2.setPointSize(12)
        self.MessageEdit.setFont(font2)

        self.verticalLayout.addWidget(self.MessageEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.seniorEditorPbtn = QPushButton(self.widget)
        self.seniorEditorPbtn.setObjectName(u"seniorEditorPbtn")

        self.horizontalLayout.addWidget(self.seniorEditorPbtn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.sendPbtn = QPushButton(self.widget)
        self.sendPbtn.setObjectName(u"sendPbtn")
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(False)
        self.sendPbtn.setFont(font3)

        self.verticalLayout.addWidget(self.sendPbtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.verticalLayout_2.addWidget(self.widget)


        self.retranslateUi(Send)

        QMetaObject.connectSlotsByName(Send)
    # setupUi

    def retranslateUi(self, Send):
        Send.setWindowTitle(QCoreApplication.translate("Send", u"CallYou", None))
        self.titleLabel.setText(QCoreApplication.translate("Send", u"CallYou\u53d1\u9001\u7aef", None))
        self.aboutPbtn.setText(QCoreApplication.translate("Send", u"\u5173\u4e8e", None))
        self.label_2.setText(QCoreApplication.translate("Send", u"\u4f60\u8981\u53d1\u9001\u4ec0\u4e48\u5462\uff1f", None))
        self.seniorEditorPbtn.setText(QCoreApplication.translate("Send", u"\u9ad8\u7ea7\u7f16\u8f91\u5668", None))
        self.sendPbtn.setText(QCoreApplication.translate("Send", u"\u53d1\u5c04\uff01", None))
    # retranslateUi

