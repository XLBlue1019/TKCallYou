# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI_SeniorEditor.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (CheckBox, PlainTextEdit, PushButton, TransparentPushButton)

class Ui_SeniorEditor(object):
    def setupUi(self, SeniorEditor):
        if not SeniorEditor.objectName():
            SeniorEditor.setObjectName(u"SeniorEditor")
        SeniorEditor.resize(271, 189)
        SeniorEditor.setMinimumSize(QSize(271, 189))
        font = QFont()
        font.setFamilies([u"\u963f\u91cc\u5df4\u5df4\u666e\u60e0\u4f53 3.0 55 Regular"])
        SeniorEditor.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(SeniorEditor)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(SeniorEditor)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleLabel = QLabel(self.widget)
        self.titleLabel.setObjectName(u"titleLabel")
        font1 = QFont()
        font1.setFamilies([u"\u963f\u91cc\u5df4\u5df4\u666e\u60e0\u4f53 3.0 95 ExtraBold"])
        font1.setPointSize(18)
        font1.setBold(True)
        self.titleLabel.setFont(font1)

        self.verticalLayout.addWidget(self.titleLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.option1CheckBox = CheckBox(self.widget)
        self.option1CheckBox.setObjectName(u"option1CheckBox")

        self.horizontalLayout.addWidget(self.option1CheckBox)

        self.option1WenHao = TransparentPushButton(self.widget)
        self.option1WenHao.setObjectName(u"option1WenHao")

        self.horizontalLayout.addWidget(self.option1WenHao)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.option2CheckBox = CheckBox(self.widget)
        self.option2CheckBox.setObjectName(u"option2CheckBox")

        self.horizontalLayout.addWidget(self.option2CheckBox)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.plainTextEdit = PlainTextEdit(self.widget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.verticalLayout.addWidget(self.plainTextEdit)

        self.sendPbtn = PushButton(self.widget)
        self.sendPbtn.setObjectName(u"sendPbtn")

        self.verticalLayout.addWidget(self.sendPbtn)


        self.verticalLayout_2.addWidget(self.widget)


        self.retranslateUi(SeniorEditor)

        QMetaObject.connectSlotsByName(SeniorEditor)
    # setupUi

    def retranslateUi(self, SeniorEditor):
        SeniorEditor.setWindowTitle(QCoreApplication.translate("SeniorEditor", u"Form", None))
        self.titleLabel.setText(QCoreApplication.translate("SeniorEditor", u"\u9ad8\u7ea7\u7f16\u8f91\u5668", None))
        self.option1CheckBox.setText(QCoreApplication.translate("SeniorEditor", u"\u8981\u6c42\u63a5\u6536\u7aef\u786e\u5b9a\u6536\u5230", None))
        self.option1WenHao.setText(QCoreApplication.translate("SeniorEditor", u"\uff1f", None))
        self.option2CheckBox.setText(QCoreApplication.translate("SeniorEditor", u"\u542f\u7528\u8bed\u97f3", None))
        self.sendPbtn.setText(QCoreApplication.translate("SeniorEditor", u"\u53d1\u5c04\uff01", None))
    # retranslateUi

